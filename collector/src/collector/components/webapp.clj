(ns collector.components.webapp
  (:require [com.stuartsierra.component :as component]
            [ring.adapter.jetty :as jetty]
            [ring.middleware.json :refer [wrap-json-body wrap-json-response]]
            [ring.middleware.params :refer [wrap-params]]
            [ring.middleware.keyword-params :refer [wrap-keyword-params]]
            [compojure.core :refer [defroutes POST GET]]
            [compojure.route :as route]
            [collector.controllers.decisions :as decisions]
            [ring.util.response :as response]))

(defn create-routes [database]
  (defroutes app-routes
    (POST "/decisions" request (decisions/create-decision-handler database request))
    (GET "/decisions/:customer-id" request (decisions/get-decision-handler database request))
    (GET "/decisions" request (decisions/get-all-decisions-handler database request))
    (GET "/health" [] (response/response {:status "ok"}))
    (route/not-found {:error "Not Found"})))

(defn create-app [database]
  (-> (create-routes database)
      (wrap-keyword-params)
      (wrap-params)
      (wrap-json-body {:keywords? true})
      (wrap-json-response)))

(defrecord WebApp [database port server]
  component/Lifecycle
  (start [this]
    (println "Starting web server on port" (or port 3000))
    (let [app (create-app database)
          server (jetty/run-jetty app {:port (or port 3000) :join? false})]
      (assoc this :server server)))
  
  (stop [this]
    (when server
      (println "Stopping web server")
      (.stop server))
    (assoc this :server nil)))

(defn new-webapp
  ([] (new-webapp 3000))
  ([port] (->WebApp nil port nil)))

