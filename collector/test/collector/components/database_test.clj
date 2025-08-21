(ns collector.components.database-test
  (:require [clojure.test :refer :all]
            [com.stuartsierra.component :as component]
            [collector.components.database :as db]
            [collector.models.decision :as decision]))

(deftest test-in-memory-database
  (testing "Database component lifecycle"
    (let [database (db/new-in-memory-database)
          started-db (component/start database)]
      (is (some? (:data started-db)))
      (is (instance? clojure.lang.Atom (:data started-db)))
      
      (let [stopped-db (component/stop started-db)]
        (is (nil? (:data stopped-db))))))
  
  (testing "Save and retrieve decision"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (random-uuid)
          decision-record (decision/create-decision-record 
                          customer-id 
                          :application 
                          {:score 85 :approved true})]
      
      ;; Save decision
      (let [saved-record (db/save-decision! database decision-record)]
        (is (= decision-record saved-record)))
      
      ;; Retrieve decision
      (let [retrieved-record (db/get-decision database customer-id)]
        (is (= decision-record retrieved-record)))
      
      ;; Get all decisions
      (let [all-decisions (db/get-all-decisions database)]
        (is (= 1 (count all-decisions)))
        (is (= decision-record (first all-decisions))))))
  
  (testing "Save multiple decisions"
    (let [database (component/start (db/new-in-memory-database))
          customer-id-1 (random-uuid)
          customer-id-2 (random-uuid)
          decision-1 (decision/create-decision-record customer-id-1 :application {:score 85})
          decision-2 (decision/create-decision-record customer-id-2 :lobby {:score 92})]
      
      (db/save-decision! database decision-1)
      (db/save-decision! database decision-2)
      
      (let [all-decisions (db/get-all-decisions database)]
        (is (= 2 (count all-decisions)))
        (is (contains? (set all-decisions) decision-1))
        (is (contains? (set all-decisions) decision-2)))))
  
  (testing "Retrieve non-existent decision returns nil"
    (let [database (component/start (db/new-in-memory-database))
          non-existent-id (random-uuid)]
      (is (nil? (db/get-decision database non-existent-id)))))
  
  (testing "Save invalid decision throws exception"
    (let [database (component/start (db/new-in-memory-database))
          invalid-record {:customer-id "not-a-uuid"
                         :decision-type :application
                         :data-decision {:score 85}}]
      (is (thrown? Exception (db/save-decision! database invalid-record)))))
  
  (testing "Overwrite existing decision"
    (let [database (component/start (db/new-in-memory-database))
          customer-id (random-uuid)
          decision-1 (decision/create-decision-record customer-id :application {:score 85})
          decision-2 (decision/create-decision-record customer-id :lobby {:score 92})]
      
      (db/save-decision! database decision-1)
      (db/save-decision! database decision-2)
      
      (let [retrieved-record (db/get-decision database customer-id)
            all-decisions (db/get-all-decisions database)]
        (is (= decision-2 retrieved-record))
        (is (= 1 (count all-decisions)))))))

