(ns collector.models.decision-test
  (:require [clojure.test :refer :all]
            [collector.models.decision :as decision]
            [clj-time.core :as time]))

(deftest test-create-decision-record
  (testing "Creating a valid decision record"
    (let [customer-id (random-uuid)
          decision-type :application
          data-decision {:score 85 :approved true}
          record (decision/create-decision-record customer-id decision-type data-decision)]
      (is (= customer-id (:customer-id record)))
      (is (= decision-type (:decision-type record)))
      (is (= data-decision (:data-decision record)))
      (is (instance? org.joda.time.DateTime (:created-at record)))))
  
  (testing "Creating decision record with different decision types"
    (doseq [decision-type [:application :lobby :registration-base :registration-complement]]
      (let [customer-id (random-uuid)
            data-decision {:test true}
            record (decision/create-decision-record customer-id decision-type data-decision)]
        (is (= decision-type (:decision-type record))))))
  
  (testing "Creating decision record with complex data-decision"
    (let [customer-id (random-uuid)
          decision-type :registration-complement
          data-decision {:personal-info {:name "John" :age 30}
                        :documents [:passport :license]
                        :score 92.5
                        :verified true}
          record (decision/create-decision-record customer-id decision-type data-decision)]
      (is (= data-decision (:data-decision record)))))
  
  (testing "Invalid decision type should throw assertion error"
    (let [customer-id (random-uuid)
          invalid-decision-type :invalid-type
          data-decision {:test true}]
      (is (thrown? AssertionError
                   (decision/create-decision-record customer-id invalid-decision-type data-decision)))))
  
  (testing "Invalid customer-id should throw assertion error"
    (let [invalid-customer-id "not-a-uuid"
          decision-type :application
          data-decision {:test true}]
      (is (thrown? AssertionError
                   (decision/create-decision-record invalid-customer-id decision-type data-decision)))))
  
  (testing "Invalid data-decision should throw assertion error"
    (let [customer-id (random-uuid)
          decision-type :application
          invalid-data-decision "not-a-map"]
      (is (thrown? AssertionError
                   (decision/create-decision-record customer-id decision-type invalid-data-decision))))))

(deftest test-valid-decision-record?
  (testing "Valid decision record"
    (let [record {:customer-id (random-uuid)
                  :decision-type :application
                  :data-decision {:score 85}
                  :created-at (time/now)}]
      (is (decision/valid-decision-record? record))))
  
  (testing "Invalid decision record - missing fields"
    (let [record {:customer-id (random-uuid)
                  :decision-type :application}]
      (is (not (decision/valid-decision-record? record)))))
  
  (testing "Invalid decision record - wrong types"
    (let [record {:customer-id "not-a-uuid"
                  :decision-type :application
                  :data-decision {:score 85}
                  :created-at (time/now)}]
      (is (not (decision/valid-decision-record? record))))))

