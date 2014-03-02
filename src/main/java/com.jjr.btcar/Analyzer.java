package com.jjr.btcar;

import org.apache.commons.collections.CollectionUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Analyzer {

    /**
     * This is for finding values that are discretely triggered (not continuous or on a range)
     * and always send out the same data.
     *
     * @param data
     */
    public Analysis beforeAfter(Results data) {

        List<String> baseline = data.getBaselinesCombined();
        List<List<String>> recordings = data.getRecordings();

        //Find only what's the same among recordings
        if (recordings.isEmpty()) {
            throw new IllegalArgumentException("No recordings!");
        }
        List<String> filtered = recordings.get(0);
        for (List<String> recording : recordings) {
            filtered = (List<String>) CollectionUtils.intersection(filtered, recording);
        }
        filtered.removeAll(baseline);


        //Count occurrences
        Map<String, Integer> counts = new HashMap<String, Integer>();
        for (String s : filtered) {
            int count = 0;

            for (List<String> recording : recordings) {
                int cardinality = CollectionUtils.cardinality(s, recording);
                count += cardinality;
            }

            counts.put(s, count);
        }

        Analysis analysis = new Analysis();
        analysis.setResults(filtered);
        analysis.setCardinalityMap(counts);
        analysis.setData(data);

        return analysis;

    }

    public class Analysis {

        private List<String> results;
        private Map<String, Integer> cardinalityMap;
        private Results data;

        public void setResults(List<String> results) {
            this.results = results;
        }

        public List<String> getResults() {
            return results;
        }

        public void setCardinalityMap(Map<String,Integer> cardinalityMap) {
            this.cardinalityMap = cardinalityMap;
        }

        public Map<String, Integer> getCardinalityMap() {
            return cardinalityMap;
        }

        public void setData(Results data) {
            this.data = data;
        }

        public Results getData() {
            return data;
        }

        public List<Integer> getCardinalityByRun(String k) {
            List<Integer> cardinality = new ArrayList<Integer>();

            for(List<String> recording : data.getRecordings()) {
                int card = CollectionUtils.cardinality(k, recording);
                cardinality.add(card);
            }

            return cardinality;
        }
    }
}
