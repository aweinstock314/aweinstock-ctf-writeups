// https://devtoolzone.com/decompiler/java

public class Hasher
{
    private static boolean hash(final String s) {
        int n = 7;
        final int n2 = 593779930;
        for (int i = 0; i < s.length(); ++i) {
            n = n * 31 + s.charAt(i);
        }
        return n == n2;
    }
    
    public static void main(final String[] array) {
        if (array.length != 1) {
            System.out.println("Usage: java Hasher <password>");
            System.exit(1);
        }
        if (hash(array[0])) {
            System.out.println("Correct");
        }
        else {
            System.out.println("Incorrect");
        }
    }
}
