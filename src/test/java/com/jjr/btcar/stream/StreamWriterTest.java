package com.jjr.btcar.stream;

import com.jjr.btcar.python.stream.StreamWriter;
import org.junit.Test;

import java.io.ByteArrayOutputStream;

public class StreamWriterTest {

    @Test
    public void testName() throws Exception {

        ByteArrayOutputStream stream = new ByteArrayOutputStream();

        StreamWriter writer = new StreamWriter(stream);
        Thread thread = new Thread(writer);
        thread.start();

        Thread.sleep(2000);

        writer.write("poop");
        Thread.sleep(2000);
        writer.write("onit");
        Thread.sleep(2000);
        writer.kill();

        while (thread.isAlive()) {
            System.out.println("waiting for dead");
        }
        System.out.println(stream.toString());

    }
}
