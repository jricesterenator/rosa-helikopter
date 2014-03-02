//package com.jjr.btcar;
//
//import com.jjr.btcar.p2.stream.AsyncStreamReader;
//import org.junit.Test;
//
//public class SerialTest {
//
//    private static final String DEVICE = "/dev/tty.OBDLinkMX-STN-SPP";
//
//    @Test
//    public void testName() throws Exception {
//        SerialPython serial = new SerialPython("btcar.py");
//        serial.connect(DEVICE, 115200);
//        serial.write("ATI");
//        serial.write("ATSP0");
//
//        AsyncStreamReader reader = serial.sendAsyncCommand("ATMA");
//        Thread.sleep(5000);
////        System.out.println("CURRENT OUTPUT: " + reader.getOutput().toString());
//        Thread.sleep(5000);
////        System.out.println("CURRENT OUTPUT2: " + reader.getOutput().toString());
//        reader.kill();
//        serial.write("");
//        Thread.sleep(3000);
//        System.out.println("CURRENT OUTPUT3: " + reader.getOutput().toString());
//
//
//        System.out.println("Should be no more output...");
//        Thread.sleep(5000);
//        System.out.println("CURRENT OUTPUT4: " + reader.getOutput().toString());
//
//        Thread.sleep(2000); //Make sure we get all output processed
//        serial.terminate();
//    }
//}
