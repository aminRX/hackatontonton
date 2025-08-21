(ns collector.models.decision
  (:require [schema.core :as s]
            [clj-time.core :as time]))

;; Decision type enum
(def DecisionType
  (s/enum :application :lobby :registration-base :registration-complement))

;; Decision record schema
(def DecisionRecord
  {:customer-id s/Uuid
   :decision-type DecisionType
   :data-decision {s/Keyword s/Any}
   :created-at org.joda.time.DateTime})

;; Function to create a new decision record
(defn create-decision-record
  [customer-id decision-type data-decision]
  {:pre [(uuid? customer-id)
         (contains? #{:application :lobby :registration-base :registration-complement} decision-type)
         (map? data-decision)]}
  {:customer-id customer-id
   :decision-type decision-type
   :data-decision data-decision
   :created-at (time/now)})

;; Function to validate a decision record
(defn valid-decision-record?
  [record]
  (nil? (s/check DecisionRecord record)))

