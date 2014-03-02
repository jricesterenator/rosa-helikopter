package com.jjr.btcar.reader3;

import org.junit.Test;

public class PythonProcess3Test {

    @Test
    public void testName() throws Exception {

        PythonProcess3 pp = new PythonProcess3(null);
        pp.executeInteractively();
        pp.sendCommand("print range(15)");
        pp.sendAsyncCommand("print 'hi1'");
        pp.sendCommand("print 'hi2'");
        pp.waitForAsyncToFinish();

        System.out.println("DONE");
        while(true) {
            Thread.sleep(100);
        }

    }
}
