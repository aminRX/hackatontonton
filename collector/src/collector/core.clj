(ns collector.core
  (:gen-class)
  (:require [com.stuartsierra.component :as component]
            [collector.components :as components]))

(defn -main
  "Start the collector service"
  [& args]
  (let [port (if (first args) 
               (Integer/parseInt (first args)) 
               3000)
        system (components/base-system port)]
    (println "Starting collector service on port" port)
    (component/start system)
    (println "Service started. Press Ctrl+C to stop.")
    (.addShutdownHook 
     (Runtime/getRuntime) 
     (Thread. #(do (println "Shutting down...")
                   (component/stop system))))))

