package com.jjr.btcar.python.stream;

public class DataLock {

    private volatile boolean hasData = false;

    public void setHasData(boolean hasData) {
        this.hasData = hasData;
    }

    public boolean isHasData() {
        return hasData;
    }
}
