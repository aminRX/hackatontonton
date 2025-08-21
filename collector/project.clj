(defproject collector "0.1.0-SNAPSHOT"
  :description "Microservice for collecting customer decisions"
  :url "http://example.com/collector"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [com.stuartsierra/component "1.1.0"]
                 [ring/ring-core "1.9.6"]
                 [ring/ring-jetty-adapter "1.9.6"]
                 [ring/ring-json "0.5.1"]
                 [compojure "1.7.0"]
                 [cheshire "5.12.0"]
                 [prismatic/schema "1.4.1"]
                 [clj-time "0.15.2"]]
  :profiles {:dev {:dependencies [[ring/ring-mock "0.4.0"]
                                  [org.clojure/test.check "1.1.1"]]}}
  :main ^:skip-aot collector.core
  :target-path "target/%s"
  :source-paths ["src"]
  :test-paths ["test"])

