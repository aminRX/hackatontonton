(ns collector.components
  (:require [com.stuartsierra.component :as component]
            [collector.components.database :as database]
            [collector.components.webapp :as webapp]))

(defn base-system
  ([] (base-system 3000))
  ([port]
   (component/system-map
     :database (database/new-in-memory-database)
     :webapp (component/using
               (webapp/new-webapp port)
               [:database]))))

(defn test-system
  []
  (component/system-map
    :database (database/new-in-memory-database)))

