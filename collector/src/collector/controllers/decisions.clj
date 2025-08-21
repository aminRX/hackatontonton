(ns collector.controllers.decisions
  (:require [collector.models.decision :as decision]
            [collector.components.database :as db]
            [ring.util.response :as response]
            [cheshire.core :as json]))

(defn create-decision-handler
  [database request]
  (try
    (let [{:keys [customer-id decision-type data-decision]} (:body request)
          customer-uuid (if (string? customer-id)
                          (java.util.UUID/fromString customer-id)
                          customer-id)
          decision-type-kw (if (string? decision-type)
                            (keyword decision-type)
                            decision-type)
          decision-record (decision/create-decision-record 
                          customer-uuid
                          decision-type-kw
                          data-decision)
          saved-record (db/save-decision! database decision-record)
          response-data {:customer-id (str (:customer-id saved-record))
                        :decision-type (:decision-type saved-record)
                        :data-decision (:data-decision saved-record)
                        :created-at (str (:created-at saved-record))}]
      (-> (response/response (json/generate-string response-data))
          (response/content-type "application/json")
          (response/status 201)))
    (catch IllegalArgumentException e
      (-> (response/response 
           (json/generate-string {:error "Invalid UUID format" :message (.getMessage e)}))
          (response/content-type "application/json")
          (response/status 400)))
    (catch AssertionError e
      (-> (response/response 
           (json/generate-string {:error "Invalid decision data" :message (.getMessage e)}))
          (response/content-type "application/json")
          (response/status 400)))
    (catch Exception e
      (-> (response/response 
           (json/generate-string {:error "Internal server error" :message (.getMessage e)}))
          (response/content-type "application/json")
          (response/status 500)))))

(defn get-decision-handler
  [database request]
  (try
    (let [customer-id-str (get-in request [:params :customer-id])
          customer-uuid (java.util.UUID/fromString customer-id-str)
          decision-record (db/get-decision database customer-uuid)]
      (if decision-record
        (let [response-data {:customer-id (str (:customer-id decision-record))
                            :decision-type (:decision-type decision-record)
                            :data-decision (:data-decision decision-record)
                            :created-at (str (:created-at decision-record))}]
          (-> (response/response (json/generate-string response-data))
              (response/content-type "application/json")))
        (-> (response/response 
             (json/generate-string {:error "Decision not found"}))
            (response/content-type "application/json")
            (response/status 404))))
    (catch IllegalArgumentException e
      (-> (response/response 
           (json/generate-string {:error "Invalid UUID format" :message (.getMessage e)}))
          (response/content-type "application/json")
          (response/status 400)))
    (catch Exception e
      (-> (response/response 
           (json/generate-string {:error "Internal server error" :message (.getMessage e)}))
          (response/content-type "application/json")
          (response/status 500)))))

(defn get-all-decisions-handler
  [database request]
  (try
    (let [decisions (db/get-all-decisions database)
          response-data (map (fn [record]
                              {:customer-id (str (:customer-id record))
                               :decision-type (:decision-type record)
                               :data-decision (:data-decision record)
                               :created-at (str (:created-at record))})
                            decisions)]
      (-> (response/response (json/generate-string response-data))
          (response/content-type "application/json")))
    (catch Exception e
      (-> (response/response 
           (json/generate-string {:error "Internal server error" :message (.getMessage e)}))
          (response/content-type "application/json")
          (response/status 500)))))
