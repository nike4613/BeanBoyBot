package bbb;

import java.io.File;
import java.util.ArrayList;

import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

public class StreamMessage implements Runnable{
	
	private static ArrayList<String> messages = new ArrayList<String>();
	private static File soundEffect = new File("MessageSound.wav");
	
	public void run() {
		while(TwitchChat.connected) {
			if(messages.size() > 0) {
				String message = messages.get(0);
				messages.remove(0);
				playSound(soundEffect, false);
				FileHandler.writeToFile("StreamMessage", message);
				try {
					Thread.sleep(12000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				FileHandler.writeToFile("StreamMessage", "");
			}
			else {
				try {
					Thread.sleep(1000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
	}
	
	public static void add(String user, String message) {
		if(PlayersHandler.getPoints(user) >= 1000) {
			if(message.length() <= 280) {
				PlayersHandler.removePoints(user, 1000);
				messages.add(user + ": " + message.substring(12));
				TwitchChat.outsideMessage("Your message has been added "+
							"to the queue, " + user + ".");
			}
			else {
				TwitchChat.outsideMessage("Sorry, " + user + ", but there "+
						"is a 280 character limit on messages.");
			}
			
		}
		else {
			TwitchChat.outsideMessage("Sorry, " + user + ", but it "+
						"it costs 1000 points to buy a message.");
		}
	}
	
	// Credit to: https://www.youtube.com/watch?v=QVrxiJyLTqU for help
	private static void playSound(File soundFile, boolean synchronous) {
		try {
			Clip clip = AudioSystem.getClip();
			clip.open(AudioSystem.getAudioInputStream(soundFile));
			clip.start();
			if(synchronous)
				Thread.sleep(clip.getMicrosecondLength() / 1000);
		}catch(Exception e) {
			System.err.println("Error with sound: " + e);
		}
	}
}
