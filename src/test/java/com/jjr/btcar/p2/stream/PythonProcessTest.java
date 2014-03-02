package com.jjr.btcar.p2.stream;

import com.jjr.btcar.python.PythonProcess;
import org.junit.Test;

public class PythonProcessTest {

    @Test
    public void testExecute() throws Exception {

        PythonProcess pp = new PythonProcess("");
        pp.executeInteractively();
        pp.execute("print range(1,1500)");


//        Thread.sleep(1000);
        System.out.println();
        pp.terminate();

    }
}
