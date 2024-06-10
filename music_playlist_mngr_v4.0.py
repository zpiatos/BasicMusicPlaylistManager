import os

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.next = None

class MusicPlaylist:
    def __init__(self, name, version="v3v4"):
        self.name = name
        self.head = None
        self.version = version

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def add_song(self, title, artist): 
        new_song = Song(title, artist)
        if not self.head:
            self.head = new_song
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_song

    def search_song(self, search_input):
        if not isinstance(search_input, str): 
            print("Error: Search input must be a string.")
            return
        elif not search_input.strip():  
            print("Error: Search input cannot be empty.")
            return

    def remove_song(self):
        if not self.head:
            return

        while True:
            try:
                position = input("Enter position of the song to remove: ")
                if not position:
                    raise ValueError("Position cannot be empty.")

                position = int(position)
                if position < 1:
                    raise ValueError("Position must be a positive integer.")

                current = self.head
                if position == 1:
                    removed_song = self.head.title
                    self.head = self.head.next
                    print(f"{removed_song} has been removed.")
                    return

                for _ in range(position - 2):
                    if current.next:
                        current = current.next
                    else:
                        raise ValueError("Position out of range.")

                if not current.next:
                    raise ValueError("Position out of range.")

                removed_song = current.next.title
                current.next = current.next.next
                print(f"{removed_song} has been removed.")
                return

            except ValueError:
                print("Invalid input.")

    def display_playlist(self):
        try:
            if not self.head:
                raise ValueError("Playlist is empty.")

            while True:
                display_choice = input("Display (O)riginal or (S)orted playlist?: ").lower()
                if display_choice in ("o", "s"):
                    break
                else:
                    print("Invalid choice. Please enter 'o' or 's'.")

            if display_choice == "o":
                current = self.head
                position = 1
                print(self.name)
                while current:
                    print(f"{position}. {current.title} - {current.artist}")
                    current = current.next
                    position += 1
            elif display_choice == "s":
                while True:
                    sort_by = input("Sort by (T)itle or (A)rtist?: ").lower()
                    if sort_by in ("t", "a"):
                        break
                    else:
                        print("Invalid choice. Please enter 't' or 'a'.")

                sorted_songs = sorted(list(self), key=lambda song: song.title.casefold() if sort_by == "t" else song.artist.casefold())
                
                print(self.name + " (Sorted)")
                for i, song in enumerate(sorted_songs):
                    if sort_by == "t":
                        print(f"{i+1}. {song.title} - {song.artist}")
                    elif sort_by == "a":
                        print(f"{i+1}. {song.artist} - {song.title}")

        except ValueError as e:
            print(f"{e}")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playlists = []

class MusicPlaylistManager: # PABAGO NG PATH TAS KEEP NIYO YUNG "user_infos.txt"
    def __init__(self, filename="C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\user_infos.txt", version="v3v4"):
        self.users = []
        self.filename = filename
        self.version = version
        if not os.path.exists(self.filename):
            self.create_users_file()
        self.load_users()

    def create_users_file(self):
        try:
            with open(self.filename, "w") as file:
                pass
        except Exception as e:
            print(f"Error creating users file: {e}")

    def load_users(self):
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    username, password = line.strip().split(",")
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def save_users(self):
        try:
            with open(self.filename, "w") as file:
                for user in self.users:
                    file.write(f"{user.username},{user.password}\n")
        except Exception as e:  
            print(f"Error saving users: {e}")

    def validation(self, value):
        if not value or value.isspace():
            return False

        has_letter = False
        has_digit = False

        for char in value:
            if char.isalpha():
                has_letter = True
            elif char.isdigit():
                has_digit = True
            else: 
                return False

        return has_letter and has_digit

    def sign_up(self):
        special_chars = set("!@#$%^&*()_+-?;""`~/,=[]}{\|'") - set(" ")

        while True:
            try:
                while True:  
                    try:
                        username = input("Enter your username: ")

                        if not username.strip() or " " in username:
                            raise ValueError("Username cannot be empty, have spaces, or consist only of spaces.")

                        if len(username) < 8:
                            raise ValueError("Username must be at least 8 characters long.")
                        
                        if not (any(c.isalpha() for c in username) and
                                any(c.isdigit() for c in username)):
                            raise ValueError("Username must contain at least one letter, nad one digit (excluding space).")

                        for user in self.users:
                            if user.username == username:
                                raise ValueError("Username already exists. Please choose another one.")

                        break
                    except ValueError as e:
                        print(f"{e}")

                while True:  
                    try:
                        password = input("Enter your password: ")

                        if not password.strip():
                            raise ValueError("Password cannot be empty or consist only of spaces.")

                        if len(password) < 8:
                            raise ValueError("Password must be at least 8 characters long.")

                        if not (any(c.isalpha() for c in password) and
                                any(c.isdigit() for c in password) and
                                any(c in special_chars for c in password)):
                            raise ValueError("Password must contain at least one letter, one digit, and one special character (excluding space and comma).")

                        break
                    except ValueError as e:
                        print(f"{e}")

                new_user = User(username, password)
                self.users.append(new_user)
                self.save_users()  
                print("Account created successfully.")
                return

            except ValueError as e:
                print(f"{e}")

    def log_in(self):
        while True:
            try:
                username = input("Enter your username: ")
                if not username.strip():
                    raise ValueError("Username cannot be empty.")

                password = input("Enter your password: ")
                if not password.strip():
                    raise ValueError("Password cannot be empty.")

                for user in self.users:
                    if user.username == username and user.password == password:
                        print(f"You are now logged in as {username}.")
                        return user 

                raise ValueError("Invalid username or password.")

            except ValueError as e:
                print(f"{e}")
                return None

    def create_playlist(self):
        while True:
            name = input("Enter playlist name: ")
            if name.strip():  
                break
            else:
                print("Playlist name cannot be empty. Please try again.")
        print("Playlist created successfully.")
        return MusicPlaylist(name)

    def load_playlists(self, username): 
        user_playlists = []
        playlist_dir = "C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists" 
        for filename in os.listdir(playlist_dir):
            if filename.startswith(username + "_") and filename.endswith(f"_{self.version}.txt"):
                playlist = self.load_playlist(os.path.join(playlist_dir, filename))
                if playlist:
                    user_playlists.append(playlist)
        return user_playlists
    
    def load_playlist(self, filename): 
        try:
            with open(filename, "r") as f:
                playlist_name = f.readline().strip()
                playlist = MusicPlaylist(playlist_name, self.version)
                for line in f:
                    title, artist = line.strip().split(",")
                    playlist.add_song(title, artist)
                return playlist
        except FileNotFoundError:
            return None

    def save_playlist(self, user, playlist): 
        filename = os.path.join("C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists", 
                                f"{user.username}_{playlist.name}_{self.version}.txt")
        try:
            with open(filename, "w") as f:
                f.write(f"{playlist.name}\n")
                for song in playlist:
                    f.write(f"{song.title},{song.artist}\n")
        except Exception as e:
            print(f"Error saving playlist: {e}")
    
    def add_song_to_playlists(self, user, title, artist):
        if not user.playlists:
            print("You don't have any playlists yet. Please create one first.")
            return

        print("\nYour Playlists:")
        for i, playlist in enumerate(user.playlists):
            print(f"{i+1}. {playlist.name}")

        while True:
            try:
                choices_str = input("Enter playlist numbers to add the song (comma-separated): ")
                choices = []
                for choice_str in choices_str.split(","): 
                    choice = choice_str.strip()  

                    if choice.isdigit():
                        choices.append(int(choice) - 1)
                    else:
                        raise ValueError("Invalid playlist choice. Only integers are allowed.")

                unique_choices = []
                for choice in choices:
                    if 0 <= choice < len(user.playlists) and choice not in unique_choices:
                        unique_choices.append(choice)
                    else:
                        raise ValueError("Invalid or duplicate playlist choice.")

                for choice in unique_choices:
                    current = user.playlists[choice].head
                    while current:
                        if current.title == title and current.artist == artist:
                            print(f"Song '{title}' by '{artist}' is already in playlist '{user.playlists[choice].name}'.")
                            break
                        current = current.next
                    else:
                        user.playlists[choice].add_song(title, artist)
                        self.save_playlist(user, user.playlists[choice])
                        print(f"Song added to '{user.playlists[choice].name}' successfully.")
                break

            except ValueError as e:
                print(f"{e}")

    def search_all_playlists(self, user, search_input, search_by):
        if not isinstance(search_input, str): 
            print("Error: Search input must be a string.")
            return
        elif not search_input.strip(): 
            print("Error: Search input cannot be empty.")
            return
        
        search_input_folded = search_input.casefold()
        found_songs = []

        for playlist in user.playlists:
            current = playlist.head
            position = 1

            while current:
                if search_by == "t" and search_input_folded in current.title.casefold():
                    found_songs.append((playlist.name, position, current.title, current.artist))
                elif search_by == "a" and search_input_folded in current.artist.casefold():
                    found_songs.append((playlist.name, position, current.title, current.artist))
                current = current.next
                position += 1

        if not found_songs:
            print("No matching songs found in your playlists.")
        else:
            print("Found songs:")
            for playlist_name, position, title, artist in found_songs:
                print(f"Found at {playlist_name}: {position}. {title} by {artist}")

    def create_new_playlist(self, user):
        while True:
            name = input("Enter new playlist name: ")
            if name.strip():

                if any(playlist.name == name for playlist in user.playlists):
                    print("A playlist with this name already exists. Please choose another name.")
                else:
                    filename = os.path.join("C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists", 
                                            f"{user.username}_{name}_{self.version}.txt")

                    if not os.path.exists(filename): 
                        new_playlist = MusicPlaylist(name)
                        user.playlists.append(new_playlist)
                        self.save_playlist(user, new_playlist)
                        print("New playlist created successfully.")
                        break
                    else:
                        print("A playlist file with this name already exists. Please choose another name.")

            else:
                print("Playlist name cannot be empty. Please try again.")

    def main_menu(self, user):
        user.playlists = self.load_playlists(user.username)
        
        while True:
            print("\nChoices:")
            print("A. Add Song to Playlist(s)")
            print("B. Remove Song from Playlist")
            print("C. Search Song or Artist from Playlist")
            print("D. Display Playlist")
            print("E. Create New Playlist")
            print("F. Delete Playlist") 
            print("G. Delete Account")
            print("H. Log Out")

            choice = input("Enter your choice: ").casefold()

            if choice == "a":
                while True:
                    try:
                        title = input("Enter song title: ")
                        if not title.strip():
                            raise ValueError("Song title cannot be empty or consist only of spaces.")

                        artist = input("Enter artist name: ")
                        if not artist.strip():
                            raise ValueError("Artist name cannot be empty or consist only of spaces.")

                        self.add_song_to_playlists(user, title, artist)
                        break 
                    except ValueError as e:
                        print(f"{e}")
                
            elif choice == 'b':
                if user.playlists: 
                    print("\nYour Playlists:")
                    for i, playlist in enumerate(user.playlists):
                        print(f"{i+1}. {playlist.name}")

                    while True:
                        try:
                            playlist_choice = int(input("Choose a playlist to remove a song from: ")) - 1
                            if 0 <= playlist_choice < len(user.playlists):
                                user.playlists[playlist_choice].display_playlist()
                                user.playlists[playlist_choice].remove_song()
                                self.save_playlist(user, user.playlists[playlist_choice])
                                break
                            else:
                                raise ValueError("Invalid playlist choice.")
                        except ValueError as e:
                            print(f"{e}")
                else:
                    print("You don't have any playlists yet.")

            elif choice == "c":  
                if not user.playlists:
                    print("You don't have any playlists yet.")
                else:
                    while True:
                        try:
                            search_by = input("Search by (T)itle or (A)rtist?: ").lower()
                            if search_by not in ("t", "a"):
                                raise ValueError("Invalid search type. Please enter 'title' or 'artist'.")

                            if search_by == "t":
                                search_input = input("Enter the song title to search: ")
                            elif search_by == "a":
                                search_input = input("Enter the song artist to search: ")
                                
                            if not isinstance(search_input, str): 
                                raise ValueError("Error: Search input must be a string.")
                            elif not search_input.strip():  
                                raise ValueError("Error: Search input cannot be empty.")
                            
                            self.search_all_playlists(user, search_input, search_by)
                            break  
                        except ValueError as e:
                            print(f"{e}")

            elif choice == "d":
                if user.playlists:
                    print("\nYour Playlists:")
                    for i, playlist in enumerate(user.playlists):
                        print(f"{i+1}. {playlist.name}")

                    while True:
                        try:
                            playlist_choice_str = input("Choose a playlist to display: ") 
                            if not playlist_choice_str.isdigit(): 
                                raise ValueError("Invalid playlist choice. Please enter a number.")
                            playlist_choice = int(playlist_choice_str) - 1
                            if 0 <= playlist_choice < len(user.playlists):
                                user.playlists[playlist_choice].display_playlist()
                                break
                            else:
                                raise ValueError("Invalid playlist choice. Please enter a valid number.")
                        except ValueError as e:
                            print(f"{e}")
                else:
                    print("You don't have any playlists yet.")

            elif choice == "e":  
                self.create_new_playlist(user)

            elif choice == "f": # dlt pl
                if user.playlists:
                    print("\nYour Playlists:")
                    for i, playlist in enumerate(user.playlists):
                        print(f"{i+1}. {playlist.name}")

                    while True:
                        try:
                            choice = int(input("Enter the number of the playlist to delete: ")) - 1
                            if 0 <= choice < len(user.playlists):
                                playlist_to_delete = user.playlists.pop(choice)
                                if not self.delete_playlist(user, playlist_to_delete.name): 
                                    user.playlists.insert(choice, playlist_to_delete)  
                                break 
                            else:
                                raise ValueError("Invalid playlist choice.")
                        except ValueError as e:
                            print(f"{e}")

                else:
                    print("You don't have any playlists to delete.") 

            elif choice == "g": 
                if self.delete_account(user):
                    print("Account deleted successfully.")
                    break

            elif choice == "h":
                for playlist in user.playlists:  
                    self.save_playlist(user, playlist)
                print(f"Logging out {user.username}...")
                return 
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while True:
            print("\nWelcome to Music Playlist Manager! (v4)")
            print("Choices:")
            print("1. Sign Up")
            print("2. Log In")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.sign_up()
            elif choice == "2":
                user = self.log_in()
                if user:
                    self.main_menu(user)
            elif choice == "3":
                print("Exiting Music Playlist Manager. Thank you!")
                if len(self.users) > 0:
                    user = self.users[-1]
                    for playlist in user.playlists:  
                        self.save_playlist(user, playlist)
                break
            else:
                print("Invalid choice. Please try again.")

    def delete_playlist(self, user, playlist_name):
        while True:
            confirmation = input(f"Are you sure you want to delete the playlist '{playlist_name}'? (y/n): ").lower()
            if confirmation == "y":
                filename = os.path.join("C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists", 
                                        f"{user.username}_{playlist_name}_{self.version}.txt")
                if os.path.exists(filename):
                    try:
                        os.remove(filename)
                        print(f"Playlist '{playlist_name}' deleted successfully.")
                        return True
                    except Exception as e:
                        print(f"Error deleting playlist: {e}")
                        return False
                else:
                    print(f"Playlist '{playlist_name}' not found.")
                    return False
            elif confirmation == "n":
                print("Deleting playlist cancelled.")
                return False  
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    def delete_account(self, user):
        while True:
            confirmation = input(f"Are you sure you want to delete your account '{user.username}'? (y/n): ").lower()
            if confirmation in ("y", "n"):
                break
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

        if confirmation == 'y':
            self.users.remove(user)
            self.save_users()

            playlist_dir = "C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists"  

            for filename in os.listdir(playlist_dir):
                if filename.startswith(user.username + "_"):
                    playlist_path = os.path.join(playlist_dir, filename)
                    try:
                        os.remove(playlist_path)
                        print(f"Playlist '{filename}' deleted successfully.")
                    except Exception as e:
                        print(f"Error deleting playlist '{filename}': {e}")

            return True
        else:
            print("Deleting account cancelled.")
            return False
    
# main
manager = MusicPlaylistManager(version="v3v4")
manager.run()
