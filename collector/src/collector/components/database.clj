(ns collector.components.database
  (:require [com.stuartsierra.component :as component]
            [collector.models.decision :as decision]))

(defprotocol DatabaseProtocol
  (save-decision! [this decision-record])
  (get-decision [this customer-id])
  (get-all-decisions [this]))

(defrecord InMemoryDatabase [data]
  component/Lifecycle
  (start [this]
    (println "Starting in-memory database")
    (assoc this :data (atom {})))
  
  (stop [this]
    (println "Stopping in-memory database")
    (assoc this :data nil))
  
  DatabaseProtocol
  (save-decision! [this decision-record]
    (when-not (decision/valid-decision-record? decision-record)
      (throw (ex-info "Invalid decision record" {:record decision-record})))
    (let [customer-id (:customer-id decision-record)]
      (swap! data assoc customer-id decision-record)
      decision-record))
  
  (get-decision [this customer-id]
    (get @data customer-id))
  
  (get-all-decisions [this]
    (vals @data)))

(defn new-in-memory-database
  []
  (->InMemoryDatabase nil))

