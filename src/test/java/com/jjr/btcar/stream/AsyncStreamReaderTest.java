//package com.jjr.btcar.stream;
//
//import DataLock;
//import StreamReader;
//import org.junit.Test;
//
//import java.io.ByteArrayInputStream;
//
//public class AsyncStreamReaderTest {
//
//    @Test
//    public void testName() throws Exception {
//
//        ByteArrayInputStream is = new ByteArrayInputStream("lalsantohe uh aohnet et nteh teal".getBytes());
//
//        StreamReader reader = new StreamReader(is);
//        Thread thread = new Thread(reader);
//        thread.start();
//
//        Thread.sleep(2000);
//        System.out.println(reader.stopRecording());
//        reader.startRecording(new DataLock());
////        reader.setIn(new ByteArrayInputStream("this si new text".getBytes()));
//        Thread.sleep(2000);
//        System.out.println(reader.stopRecording());
//        Thread.sleep(2000);
//
//        reader.kill();
//
//        System.out.println("waiting for death");
//        while (thread.isAlive()) {
//        }
//        System.out.println("dead");
//
//    }
//}
