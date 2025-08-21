(ns collector.controllers.decisions-test
  (:require [clojure.test :refer :all]
            [com.stuartsierra.component :as component]
            [collector.controllers.decisions :as decisions]
            [collector.components.database :as db]
            [collector.models.decision :as decision]
            [cheshire.core :as json]
            [clojure.java.io :as io]))

(defn create-test-request [method uri body]
  {:request-method method
   :uri uri
   :body body  ; Pass the body directly as a map (simulating middleware parsing)
   :headers {"content-type" "application/json"}})

(deftest test-create-decision-handler
  (testing "Create valid decision"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (str (random-uuid))
          request-body {:customer-id customer-id
                       :decision-type "application"
                       :data-decision {:score 85 :approved true}}
          request (create-test-request :post "/decisions" request-body)
          response (decisions/create-decision-handler database request)]
      
      (is (= 201 (:status response)))
      (is (= "application/json" (get-in response [:headers "Content-Type"])))
      
      (let [response-body (json/parse-string (:body response) true)]
        (is (= customer-id (:customer-id response-body)))
        (is (= "application" (:decision-type response-body)))
        (is (= {:score 85 :approved true} (:data-decision response-body)))
        (is (some? (:created-at response-body))))))
  
  (testing "Create decision with all decision types"
    (let [database (component/start (db/new-in-memory-database))]
      (doseq [decision-type ["application" "lobby" "registration-base" "registration-complement"]]
        (let [customer-id (str (random-uuid))
              request-body {:customer-id customer-id
                           :decision-type decision-type
                           :data-decision {:test true}}
              request (create-test-request :post "/decisions" request-body)
              response (decisions/create-decision-handler database request)]
          
          (is (= 201 (:status response)))
          (let [response-body (json/parse-string (:body response) true)]
            (is (= decision-type (:decision-type response-body))))))))
  
  (testing "Create decision with invalid UUID"
    (let [database (component/start (db/new-in-memory-database))
          request-body {:customer-id "invalid-uuid"
                       :decision-type "application"
                       :data-decision {:score 85}}
          request (create-test-request :post "/decisions" request-body)
          response (decisions/create-decision-handler database request)]
      
      (is (= 400 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Invalid UUID format" (:error response-body))))))
  
  (testing "Create decision with invalid decision type"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (str (random-uuid))
          request-body {:customer-id customer-id
                       :decision-type "invalid-type"
                       :data-decision {:score 85}}
          request (create-test-request :post "/decisions" request-body)
          response (decisions/create-decision-handler database request)]
      
      (is (= 400 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Invalid decision data" (:error response-body))))))
  
  (testing "Create decision with complex data-decision"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (str (random-uuid))
          complex-data {:personal-info {:name "John" :age 30}
                       :documents ["passport" "license"]
                       :score 92.5
                       :verified true}
          request-body {:customer-id customer-id
                       :decision-type "registration-complement"
                       :data-decision complex-data}
          request (create-test-request :post "/decisions" request-body)
          response (decisions/create-decision-handler database request)]
      
      (is (= 201 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= complex-data (:data-decision response-body)))))))

(deftest test-get-decision-handler
  (testing "Get existing decision"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (random-uuid)
          decision-record (decision/create-decision-record 
                          customer-id 
                          :application 
                          {:score 85})]
      
      (db/save-decision! database decision-record)
      
      (let [request {:request-method :get
                    :uri (str "/decisions/" customer-id)
                    :params {:customer-id (str customer-id)}}
            response (decisions/get-decision-handler database request)]
        
        (is (= 200 (:status response)))
        (let [response-body (json/parse-string (:body response) true)]
          (is (= (str customer-id) (:customer-id response-body)))
          (is (= "application" (:decision-type response-body)))
          (is (= {:score 85} (:data-decision response-body)))))))
  
  (testing "Get non-existent decision"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (random-uuid)
          request {:request-method :get
                  :uri (str "/decisions/" customer-id)
                  :params {:customer-id (str customer-id)}}
          response (decisions/get-decision-handler database request)]
      
      (is (= 404 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Decision not found" (:error response-body))))))
  
  (testing "Get decision with invalid UUID"
    (let [database (component/start (db/new-in-memory-database))
          request {:request-method :get
                  :uri "/decisions/invalid-uuid"
                  :params {:customer-id "invalid-uuid"}}
          response (decisions/get-decision-handler database request)]
      
      (is (= 400 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= "Invalid UUID format" (:error response-body)))))))

(deftest test-get-all-decisions-handler
  (testing "Get all decisions when empty"
    (let [database (component/start (db/new-in-memory-database))
          request {:request-method :get :uri "/decisions"}
          response (decisions/get-all-decisions-handler database request)]
      
      (is (= 200 (:status response)))
      (let [response-body (json/parse-string (:body response) true)]
        (is (= [] response-body)))))
  
  (testing "Get all decisions with multiple records"
    (let [database (component/start (db/new-in-memory-database))
          customer-id-1 (random-uuid)
          customer-id-2 (random-uuid)
          decision-1 (decision/create-decision-record customer-id-1 :application {:score 85})
          decision-2 (decision/create-decision-record customer-id-2 :lobby {:score 92})]
      
      (db/save-decision! database decision-1)
      (db/save-decision! database decision-2)
      
      (let [request {:request-method :get :uri "/decisions"}
            response (decisions/get-all-decisions-handler database request)]
        
        (is (= 200 (:status response)))
        (let [response-body (json/parse-string (:body response) true)]
          (is (= 2 (count response-body)))
          (let [customer-ids (set (map :customer-id response-body))]
            (is (contains? customer-ids (str customer-id-1)))
            (is (contains? customer-ids (str customer-id-2)))))))))
