package com.jjr.btcar;

import org.junit.Test;

import java.io.File;
import java.io.FileInputStream;

public class ReaderTest {

    @Test
    public void testName() throws Exception {

        String filename = "BTCarLogfile (2014-01-18 17:12:51 +0000)";
        File file = new File("/Users/jjrice/code/BTCar-Java/logs/BTCarLogfile/" + filename);

        FileInputStream is = new FileInputStream(file);


//        FileUtils.

    }
}
