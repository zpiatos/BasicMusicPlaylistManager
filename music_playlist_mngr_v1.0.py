import os

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.next = None

class MusicPlaylist:
    def __init__(self, name, version="v1v2"):
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

    def search_song(self, search_input):
        if not search_input.strip(): 
            print("Error: Search input cannot be empty.")
            return

        search_input_folded = search_input.casefold()
        found_songs = []
        current = self.head
        position = 1

        while current:
            if search_input_folded == current.title.casefold() or search_input_folded == current.artist.casefold():
                found_songs.append((position, current.title, current.artist))
            current = current.next
            position += 1

        if not found_songs:
            print("Song not found in the playlist.")
        else:
            print("Found songs:")
            for position, title, artist in found_songs:
                print(f"Found: {position}. {title} by {artist}")

    def display_playlist(self):
        try:
            if not self.head:
                raise ValueError("Playlist is empty.")

            current = self.head
            print()
            print(self.name)
            position = 1
            while current:
                print(f"{position}. {current.title} - {current.artist}")
                current = current.next
                position += 1
        except ValueError as e:
            print(f"{e}")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playlist = None

class MusicPlaylistManager: # PABAGO NG PATH TAS KEEP NIYO "user_infos.txt"
    def __init__(self, filename="C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\user_infos.txt", version="v1v2"):
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
        special_chars = set("!@#$%^&*()_+-?"";`~/,=[]}{\|'") - set(" ")  

        while True:
            try:
                while True: 
                    try:
                        username = input("Enter your username: ")

                        if not username.strip():
                            raise ValueError("Username cannot be empty or consist only of spaces.")

                        if len(username) < 8:
                            raise ValueError("Username must be at least 8 characters long.")
                        
                        if not (any(c.isalpha() for c in username) and
                                any(c.isdigit() for c in username)):
                            raise ValueError("Username must contain at least one letter, and one digit (excluding space).")

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
                            raise ValueError("Password must contain at least one letter, one digit, and one special character (excluding space).")

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
                        user.playlist = self.load_playlist(user.username)
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
        return MusicPlaylist(name, self.version)

    def load_playlist(self, username): # gawa kayo "playlists" folder sa loob ng main folder, tas paltan niyo ng path
        filename = os.path.join("C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists",
                                f"{username}_playlist_{self.version}.txt")
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

    def save_playlist(self, user):
        if user.playlist: # gawa kayo "playlists" folder sa loob ng main folder, tas paltan niyo ng path
            filename = os.path.join("C:\\Users\\Admin\\Desktop\\Music Playlist Manager\\playlists",
                                    f"{user.username}_playlist_{self.version}.txt")
            try:
                with open(filename, "w") as f:
                    f.write(f"{user.playlist.name}\n")
                    for song in user.playlist:
                        f.write(f"{song.title},{song.artist}\n")
            except Exception as e:
                print(f"Error saving playlist: {e}")
                
    def main_menu(self, user):
        user.playlist = self.load_playlist(user.username)

        if not user.playlist: 
            user.playlist = self.create_playlist()  

        while True:
            print("\nChoices:")
            print("A. Add Song to Playlist")
            print("B. Remove Song from Playlist")
            print("C. Search Song or Artist from Playlist")
            print("D. Display Playlist")
            print("E. Log Out")

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
                    
                        user.playlist.add_song(title, artist)  
                        print("Song added successfully.")
                        self.save_playlist(user)
                        break 
                    except ValueError as e:
                        print(f"{e}")
                
            elif choice == "b":
                print()
                user.playlist.display_playlist()
                print()
                user.playlist.remove_song()
                self.save_playlist(user)

            elif choice == "c":
                if not user.playlist.head:
                    print("Playlist is empty.")
                else:
                    search_input = input("Enter the song title or artist to search: ")
                    user.playlist.search_song(search_input)

            elif choice == "d":
                print()
                if user.playlist:
                    user.playlist.display_playlist()
                else:
                    print("You don't have a playlist yet.")

            elif choice == "e":
                self.save_playlist(user)
                print(f"Logging out {user.username}...")
                break
            
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while True:
            print("\nWelcome to Music Playlist Manager! (v1)")
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
                    if user.playlist:
                        self.save_playlist(user)
                break
            else:
                print("Invalid choice. Please try again.")

# main
manager = MusicPlaylistManager(version="v1v2")
manager.run()
