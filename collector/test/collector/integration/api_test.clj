(ns collector.integration.api-test
  (:require [clojure.test :refer :all]
            [com.stuartsierra.component :as component]
            [ring.mock.request :as mock]
            [cheshire.core :as json]
            [collector.components :as components]
            [collector.components.webapp :as webapp]))

(def test-system nil)

(defn start-test-system []
  (alter-var-root #'test-system 
                  (constantly (component/start (components/test-system)))))

(defn stop-test-system []
  (when test-system
    (alter-var-root #'test-system 
                    #(component/stop %))))

(defn create-test-app []
  (let [database (:database test-system)]
    (webapp/create-app database)))

(use-fixtures :each 
  (fn [test-fn]
    (start-test-system)
    (try
      (test-fn)
    (finally
      (stop-test-system)))))

(deftest test-health-endpoint
  (testing "Health check endpoint"
    (let [app (create-test-app)
          request (mock/request :get "/health")
          response (app request)]
      
      (is (= 200 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= {:status "ok"} response-body))))))

(deftest test-create-decision-integration
  (testing "POST /decisions - Create a new decision"
    (let [app (create-test-app)
          customer-id (str (random-uuid))
          decision-data {:customer-id customer-id
                        :decision-type "application"
                        :data-decision {:score 85 :approved true :reason "Good credit score"}}
          request (-> (mock/request :post "/decisions")
                     (mock/json-body decision-data))
          response (app request)]
      
      (is (= 201 (:status response)))
      (is (= "application/json" (get-in response [:headers "Content-Type"])))
      
      (let [response-body (json/parse-string (:body response) true)]
        (is (= customer-id (:customer-id response-body)))
        (is (= "application" (:decision-type response-body)))
        (is (= (:data-decision decision-data) (:data-decision response-body)))
        (is (some? (:created-at response-body))))))
  
  (testing "POST /decisions - All decision types"
    (let [app (create-test-app)]
      (doseq [decision-type ["application" "lobby" "registration-base" "registration-complement"]]
        (let [customer-id (str (random-uuid))
              decision-data {:customer-id customer-id
                            :decision-type decision-type
                            :data-decision {:type decision-type :valid true}}
              request (-> (mock/request :post "/decisions")
                         (mock/json-body decision-data))
              response (app request)]
          
          (is (= 201 (:status response)))
          (let [response-body (json/parse-string (:body response) true)]
            (is (= decision-type (:decision-type response-body))))))))
  
  (testing "POST /decisions - Complex data-decision"
    (let [app (create-test-app)
          customer-id (str (random-uuid))
          complex-data {:personal-info {:name "María García" :age 28 :city "Madrid"}
                       :documents {:passport "ES123456789" :license "B-12345678"}
                       :financial-data {:income 45000.50 :expenses 25000.25}
                       :scores {:credit 850 :risk 0.15}
                       :flags {:verified true :premium false}
                       :tags ["new-customer" "high-value" "low-risk"]}
          decision-data {:customer-id customer-id
                        :decision-type "registration-complement"
                        :data-decision complex-data}
          request (-> (mock/request :post "/decisions")
                     (mock/json-body decision-data))
          response (app request)]
      
      (is (= 201 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= complex-data (:data-decision response-body))))))
  
  (testing "POST /decisions - Invalid UUID"
    (let [app (create-test-app)
          decision-data {:customer-id "invalid-uuid"
                        :decision-type "application"
                        :data-decision {:score 85}}
          request (-> (mock/request :post "/decisions")
                     (mock/json-body decision-data))
          response (app request)]
      
      (is (= 400 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Invalid UUID format" (:error response-body))))))
  
  (testing "POST /decisions - Invalid decision type"
    (let [app (create-test-app)
          customer-id (str (random-uuid))
          decision-data {:customer-id customer-id
                        :decision-type "invalid-type"
                        :data-decision {:score 85}}
          request (-> (mock/request :post "/decisions")
                     (mock/json-body decision-data))
          response (app request)]
      
      (is (= 400 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Invalid decision data" (:error response-body)))))))

(deftest test-get-decision-integration
  (testing "GET /decisions/:customer-id - Retrieve existing decision"
    (let [app (create-test-app)
          customer-id (str (random-uuid))
          decision-data {:customer-id customer-id
                        :decision-type "lobby"
                        :data-decision {:priority "high" :queue-position 1}}
          
          ;; First create a decision
          create-request (-> (mock/request :post "/decisions")
                            (mock/json-body decision-data))
          create-response (app create-request)]
      
      (is (= 201 (:status create-response)))
      
      ;; Then retrieve it
      (let [get-request (mock/request :get (str "/decisions/" customer-id))
            get-response (app get-request)]
        
        (is (= 200 (:status get-response)))
        (let [response-body (json/parse-string (:body get-response) true)]
          (is (= customer-id (:customer-id response-body)))
          (is (= "lobby" (:decision-type response-body)))
          (is (= (:data-decision decision-data) (:data-decision response-body)))))))
  
  (testing "GET /decisions/:customer-id - Non-existent decision"
    (let [app (create-test-app)
          customer-id (str (random-uuid))
          request (mock/request :get (str "/decisions/" customer-id))
          response (app request)]
      
      (is (= 404 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Decision not found" (:error response-body))))))
  
  (testing "GET /decisions/:customer-id - Invalid UUID"
    (let [app (create-test-app)
          request (mock/request :get "/decisions/invalid-uuid")
          response (app request)]
      
      (is (= 400 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Invalid UUID format" (:error response-body)))))))

(deftest test-get-all-decisions-integration
  (testing "GET /decisions - Empty list"
    (let [app (create-test-app)
          request (mock/request :get "/decisions")
          response (app request)]
      
      (is (= 200 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= [] response-body)))))
  
  (testing "GET /decisions - Multiple decisions"
    (let [app (create-test-app)
          decisions [{:customer-id (str (random-uuid))
                     :decision-type "application"
                     :data-decision {:score 85}}
                    {:customer-id (str (random-uuid))
                     :decision-type "lobby"
                     :data-decision {:priority "medium"}}
                    {:customer-id (str (random-uuid))
                     :decision-type "registration-base"
                     :data-decision {:step 1 :completed true}}]]
      
      ;; Create multiple decisions
      (doseq [decision-data decisions]
        (let [request (-> (mock/request :post "/decisions")
                         (mock/json-body decision-data))
              response (app request)]
          (is (= 201 (:status response)))))
      
      ;; Retrieve all decisions
      (let [request (mock/request :get "/decisions")
            response (app request)]
        
        (is (= 200 (:status response)))
        (let [response-body (json/parse-string (:body response) true)]
          (is (= 3 (count response-body)))
          (let [customer-ids (set (map :customer-id response-body))
                decision-types (set (map :decision-type response-body))]
            (is (= 3 (count customer-ids)))
            (is (contains? decision-types "application"))
            (is (contains? decision-types "lobby"))
            (is (contains? decision-types "registration-base")))))))

(deftest test-full-workflow-integration
  (testing "Complete workflow: Create, retrieve individual, retrieve all"
    (let [app (create-test-app)
          customer-id (str (random-uuid))
          decision-data {:customer-id customer-id
                        :decision-type "registration-complement"
                        :data-decision {:documents-verified true
                                       :risk-score 0.12
                                       :approval-status "pending"
                                       :metadata {:source "web" :timestamp "2024-01-01T10:00:00Z"}}}]
      
      ;; Step 1: Create decision
      (let [create-request (-> (mock/request :post "/decisions")
                              (mock/json-body decision-data))
            create-response (app create-request)]
        
        (is (= 201 (:status create-response)))
        (let [created-decision (json/parse-string (:body create-response) true)]
          (is (= customer-id (:customer-id created-decision)))
          
          ;; Step 2: Retrieve the specific decision
          (let [get-request (mock/request :get (str "/decisions/" customer-id))
                get-response (app get-request)]
            
            (is (= 200 (:status get-response)))
            (let [retrieved-decision (json/parse-string (:body get-response) true)]
              (is (= created-decision retrieved-decision))
              
              ;; Step 3: Retrieve all decisions (should contain our decision)
              (let [get-all-request (mock/request :get "/decisions")
                    get-all-response (app get-all-request)]
                
                (is (= 200 (:status get-all-response)))
                (let [all-decisions (json/parse-string (:body get-all-response) true)]
                  (is (>= (count all-decisions) 1))
                  (is (some #(= customer-id (:customer-id %)) all-decisions))))))))))))
