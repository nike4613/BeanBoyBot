package bbb;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;

import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

public class StreamEmote implements Runnable{
	
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
					String[] pieces = message.split(" ");
					FileHandler.writeToFile("StreamMessage", pieces[0]);
					String emoteName = pieces[1];
					System.out.println("Copying " + "emotes/" + emoteName + ".png" +
							" to " + "emotes/current.png");
					
					Path source = Paths.get("emotes/" + emoteName + ".png");
					Path target = Paths.get("emotes/current.png");
					Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
					Thread.sleep(8000);
				} catch (Exception e) {
					System.err.println(e);
				}
				Path source = Paths.get("emotes/blank.png");
				Path target = Paths.get("emotes/current.png");
				try {
					Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
				}catch(Exception e) {}
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
	
	private static String getEmotes() {
		File folder = new File("emotes");
		File[] listOfFiles = folder.listFiles();
		String allFileNames = "";
		for (File f : listOfFiles)
			allFileNames += f.getName();
		return allFileNames;
	}
	
	public static void add(String user, String message) {
		if(PlayersHandler.getPoints(user) >= 200) {
			String emotes = getEmotes();
			if(emotes.contains(message.substring(10))) {
				PlayersHandler.removePoints(user, 200);
				messages.add(user + ": " + message.substring(10));
				TwitchChat.outsideMessage("Your emote has been added "+
							"to the queue, " + user + ".");
			}
			else {
				TwitchChat.outsideMessage("Sorry, " + user + ", but that "+
						"emote is not available D:");
			}
			
		}
		else {
			TwitchChat.outsideMessage("Sorry, " + user + ", but it "+
						"it costs 200 points to buy an emote.");
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
