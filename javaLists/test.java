import java.io.*;
import java.util.*;

public class test {

	public static void main (String args[]) {
		test1();
		test2();

	}
	public static void test1() {
		ArrayList<Integer> a = new ArrayList<Integer>(10);
		for (int i=0;i<10;i++) {
			a.add(i);
		}
		System.out.println("added things to the array list");
		for (int i=0;i<a.size();i++) {
			System.out.print(a.get(i) + " ,");
			a.remove(i);
			// what happens when you remove indices of an arrayList while iterating over it ?
		}
		System.out.println("Printed the things in the array.. skipped some things because also removed indices as they were used ");
	}
	public static void test2() {
		ArrayList<Integer> a = new ArrayList<Integer>(10);
		for (int i=0;i<10;i++) {
			a.add(i);
		}

		System.out.println("added things to the array list");
		for (int i=a.size()-1;i>=0;i--) {
			System.out.print(a.get(i) + " ,");
			a.remove(i);
			// removing in reverse order ( from size to 0) works correctly
		}
		System.out.println("printed and removed in reverse order");
	}
}
