a = """
2023-01-15 22:25:28 INFO     discord.voice_client The voice handshake is being terminated for Channel ID 1042816985651753092 (Guild ID 1024142536517885972)
2023-01-15 22:25:28 INFO     discord.voice_client Disconnecting from voice normally, close code 1000.
2023-01-15 22:25:28 INFO     discord.player ffmpeg process 3340 has not terminated. Waiting to terminate...
2023-01-15 22:25:28 INFO     discord.player ffmpeg process 3340 should have terminated with a return code of 1.
2023-01-15 22:25:29 INFO     discord.player ffmpeg process 12000 has not terminated. Waiting to terminate...
2023-01-15 22:25:29 INFO     discord.player ffmpeg process 12000 should have terminated with a return code of 1.
2023-01-15 23:11:25 ERROR    discord.client Attempting a reconnect in 0.92s"
"""

print(a[:100])