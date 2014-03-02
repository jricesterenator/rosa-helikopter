package com.jjr.btcar;

import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;

public class Results {

    private ArrayList<List<String>> baselines = new ArrayList<List<String>>();
    private ArrayList<List<String>> recordings = new ArrayList<List<String>>();

    public void saveRun() {
        //JRTODO parse input streams and save

//        this.baselines.add(currentBaseline);
//        this.recordings.add(currentRecording);
    }

    public List<String> getBaselinesCombined() {
        ArrayList<String> combined = new ArrayList<String>();
        for(List<String> baseline : baselines) {
            combined.addAll(baseline);
        }
        return combined;
    }

    public List<List<String>> getRecordings() {
        return recordings;
    }

    public void saveRun(String runData) {
        System.out.println("GOT THIS RUN DATA:");
        System.out.println(runData);

        String delim = "\n################ BEGIN RECORDING #################\n";
        String[] split = runData.split(delim);
        String baseline = split[0];
        String recorded = split[1];

        String[] baselineData = StringUtils.split(baseline, '\n');
        List<String> baselineList = new ArrayList<String>(baselineData.length);
        CollectionUtils.addAll(baselineList, baselineData);

        String[] recordedData = StringUtils.split(recorded, '\n');
        List<String> recordedList = new ArrayList<String>(recordedData.length);
        CollectionUtils.addAll(recordedList, recordedData);

        baselines.add(baselineList);
        recordings.add(recordedList);

    }

}
