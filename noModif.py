import streamlit as st
import base64
import os
import filecmp
import random
import math
from io import BytesIO
from pydub import AudioSegment

def main():
    def create_download_link(file_content, filename):
        # Create a BytesIO object
        file_buffer = BytesIO()

        # Write the content to the BytesIO object
        file_buffer.write(file_content.encode())

        # Seek to the beginning of the buffer
        file_buffer.seek(0)

        # Encode the BytesIO object's content in base64
        b64 = base64.b64encode(file_buffer.read()).decode()

        # Generate the download link
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download hasil_enkripsi.txt</a>'

        return href

    st.sidebar.header("Menu")
    choice = st.sidebar.selectbox(
        "Select a menu", ["Tutorial","Preprocessing", "RSA"], key="menu_selectbox"
    )
    if choice == "Tutorial":
        st.title("Tutorial Penggunaan")
        st.header("1. Preprocessing")
        st.write("a. Merubah dari file ke teks base64")
        st.header("2. Enkrip dan Dekrip menggunakan RSA")
        st.write("a. Buat kunci dengan memilih page Make Keys dan catat hasilnya karena nanti akan digunakan")
        st.write("b. Jika tidak tahu kuncinya maka bisa memilih page Custom Prime, catat hasilnya untuk digunakan di page Make Keys")
        st.write("c. Enkripsi dengan memilih page Encryption")
        st.write("d. Dekripsi dengan memilih page Decryption")
        st.header("3. Preprocessing")
        st.write("a. Membuat file dari hasil dekripsi")

    elif choice == "Preprocessing":

        def binary_to_mp3(binary_data, output_path):
            # Convert binary data to BytesIO object
            binary_io = BytesIO(binary_data)

            # Read the binary data as an audio segment
            audio = AudioSegment.from_file(
                binary_io, format="raw", frame_rate=44100, channels=2, sample_width=2
            )

            # Export the audio to MP3 format
            audio.export(output_path, format="mp3")

            # Fungsi untuk membaca file dan mengonversinya ke format Base64

        def file_to_base64(file):
            # Baca file sebagai bytes
            file_binary = file.read()

            # Encode file ke dalam format Base64
            file_base64 = base64.b64encode(file_binary).decode("utf-8")

            return file_base64

        def save_base64_to_text(base64_data, output_path):
            with open(output_path, "w") as base64_file:
                base64_file.write(base64_data)

        def binarize_file_text(input_file, output_path):
            try:
                # Read the content of the input file
                content = input_file.read().decode("utf-8")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                return

            # Convert text to binary
            binary_data = " ".join(format(ord(char), "08b") for char in content)

            try:
                # Save the binary data to the output file
                with open(output_path, "w") as bin_file:
                    bin_file.write(binary_data)
                st.success(f"Binary data saved to: {output_path}")

                # Create a download link for the binary file
                download_link = create_download_link(binary_data, output_path)

                # Display the download link
                st.markdown(download_link, unsafe_allow_html=True)
            except Exception as e:
                st.warning("Fill the path to save the file")

        # Streamlit app
        st.title("File Manipulation Tool")

        # Menu
        choice = st.radio(
            "Menu",
            [
                "Merubah dari file ke teks base64",
                "Membuat file dari teks binerisasi",
            ],
        )

        if choice == "Merubah dari file ke teks base64":
            # Merubah dari file ke teks base64
            file_path = st.file_uploader(
                "Pilih file", type=["txt", "pdf", "png", "jpg", "mp3", "mp4"]
            )
            if file_path is not None:
                base64_data = file_to_base64(file_path)
                st.text("Hasil encoding Base64:")
                st.text(base64_data)

                # Menyimpan hasil encoding Base64 ke dalam file teks (opsional)
                save_choice = st.checkbox(
                    "Apakah Anda ingin menyimpan hasil encoding ke dalam file teks?"
                )
                if save_choice:
                    text_file_path = st.text_input(
                        "Masukkan path untuk menyimpan hasil encoding (contoh: hasil_encoding.txt): "
                    )
                    if st.button("Simpan"):
                        save_base64_to_text(base64_data, text_file_path)
                        st.success("File teks berhasil disimpan.")

                        # Create a download link for the original file
                        download_link = create_download_link(
                            base64_data, text_file_path
                        )

                        # Display the download link
                        st.markdown(download_link, unsafe_allow_html=True)

        elif choice == "Membuat file dari teks binerisasi":

            def binary_to_mp3(binary_data, output_path):
                try:
                    # Decode Base64 to bytes
                    binary_bytes = base64.b64decode(binary_data)
                    # Convert bytes to AudioSegment
                    audio = AudioSegment.from_file(
                        BytesIO(binary_bytes),
                        format="raw",
                        frame_rate=44100,
                        channels=2,
                        sample_width=2,
                    )
                    # Export as MP3
                    audio.export(output_path, format="mp3")
                    st.success(f"MP3 file successfully created at: {output_path}")
                except Exception as e:
                    st.error(f"Error converting binary data to MP3: {e}")

            def get_binary_file_downloader_html(binary_data, file_label):
                """
                Generates an HTML link for downloading a binary file.
                """
                # Encode binary data to base64
                b64 = base64.b64encode(binary_data).decode()
                # Create an HTML anchor tag with download attribute
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}">Download {file_label}</a>'
                return href

            binary_file = st.file_uploader("Upload Binary File", type=["txt"])
            if binary_file is not None:
                binary_data = binary_file.read()
                st.text("Binary Data:")
                st.text(binary_data)

                # Output file path
                output_file_path = st.text_input(
                    "Enter the path to save the MP3 file (including file extension): "
                )

            if st.button("Convert to MP3"):
                if output_file_path.strip() != "":
                    if binary_to_mp3(binary_data, output_file_path):
                        # Display the link to download the MP3 file
                        st.markdown(
                            get_binary_file_downloader_html(
                                binary_data, output_file_path
                            ),
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning("Please enter a valid output file path.")

        # elif choice == "Binerisasi File Teks":
        #     # Binerisasi File Teks
        #     input_path = st.file_uploader(
        #         "Pilih file teks untuk binerisasi", type=["txt"]
        #     )
        #     if input_path is not None:
        #         output_path = st.text_input(
        #             "Masukkan path untuk menyimpan hasil binerisasi (contoh: hasil_binerisasi.txt): "
        #         )
        #         binarize_file_text(input_path, output_path)
        #         st.success("File teks berhasil dibinerisasi.")

    elif choice == "RSA":
        st.title("Voice Encrypt and Decrypt Using RSA")

        # Fungsi untuk menyimpan hasil encoding Base64 ke dalam file teks
        def save_base64_to_text(base64_data, output_path):
            with open(output_path, "wb") as base64_file:
                # Convert the Base64 data to bytes
                file_binary = base64.b64decode(base64_data)
                base64_file.write(file_binary)

        # Fungsi untuk mengecek apakah suatu bilangan merupakan bilangan prima
        def is_prime(number):
            if number < 2:
                return False
            for i in range(2, number // 2 + 1):
                if number % i == 0:
                    return False
            return True

        # Fungsi untuk mencari nilai d (private key) dari nilai e (public key) dan totient n
        def mod_inverse(e, totient):
            for d in range(3, totient):
                if (d * e) % totient == 1:
                    return d
            raise ValueError("No mod inverse for e: %d, totient: %d" % (e, totient))

        def get_prime_input(message):
            user_input = st.number_input(
                message, step=1, value=3, min_value=2, key=message
            )
            while not is_prime(user_input):
                st.warning("Input is not a prime number. Please enter a prime number.")
                user_input = st.number_input(
                    message, step=1, value=3, min_value=2, key=message
                )
            return int(user_input)

        def make_key():
            st.header("RSA Key Generation")

            p = get_prime_input("Enter a prime number (p): ")
            q = get_prime_input("Enter a prime number (q): ")

            # p dan q tidak boleh sama
            while p == q:
                st.warning("p and q cannot be the same number. Please try again.")
                p = get_prime_input("Enter a prime number (p): ")
                q = get_prime_input("Enter a prime number (q): ")

            # nilai n adalah hasil perkalian p dan q dan boleh dibagikan
            n = p * q
            # nilai totient n adalah hasil perkalian p-1 dan q-1 tidak boleh dibagikan karena untuk mencari nilai d
            totient_n = (p - 1) * (q - 1)

            # nilai e adalah nilai yang tidak boleh dibagikan dan harus lebih besar dari 2 dan lebih kecil dari Pembagi persekutuan terbesar / GCD
            e = st.number_input(
                f"Enter a public exponent (e) such that 2 < e < {totient_n} and gcd(e, {totient_n}) = 1:",
                step=1,
                value=3,
                min_value=3,
                max_value=totient_n - 1,
                key="public_exponent",
            )

            while not (2 < e < totient_n and math.gcd(e, totient_n) == 1):
                st.warning("Invalid value for e. Please try again.")
                e = st.number_input(
                    f"Enter a public exponent (e) such that 2 < e < {totient_n} and gcd(e, {totient_n}) = 1:",
                    step=1,
                    value=3,
                    min_value=3,
                    max_value=totient_n - 1,
                    key="public_exponent",
                )

            d = mod_inverse(e, totient_n)

            st.success("RSA key generation successful!")
            st.write("Public key (e, n): ", e, n)
            st.write("Private key (d, n): ", d, n)

        def encryption_menu():
            max_digit = 0
            st.header("RSA Encryption")

            n = st.number_input(
                "Masukan nilai n:", min_value=1, step=1, value=1, key="encryption_n"
            )
            e = st.number_input(
                "Masukan kunci public e:",
                min_value=1,
                step=1,
                value=1,
                key="encryption_e",
            )
            input_path = st.file_uploader("Pilih file untuk dienkripsi", type=["txt"])
            process_path = st.text_input(
                "Masukkan path untuk menyimpan process enkripsi (contoh: process_enkripsi.txt):"
            )
            output_path = st.text_input(
                "Masukkan nama file untuk menyimpan hasil enkripsi (contoh: hasil_enkripsi.txt):"
            )

            if input_path is not None:
                # Baca seluruh konten file
                message = input_path.read().decode("utf-8")

                # Mengubah pesan menjadi nilai ASCII dan enkripsi
                ciphertext = []
                max_digit = 0
                values = []

                if process_path.strip() != "":
                    # Open the file in append mode
                    with open(process_path, "a") as base64_file:
                        # Iterate through each character in the message
                        for i in range(0, len(message)):
                            block = message[i]
                            encoded_block = ord(
                                block
                            )  # Convert character to ASCII value
                            encrypted_block = pow(encoded_block, e, n)

                            # Append the value to the list
                            values.append(encrypted_block)

                            # Write the details of the current block to the file
                            base64_file.write(
                                f"Block '{block}' is {encoded_block}, {encoded_block}^{e} mod {n} is {encrypted_block}\n"
                            )

                            current_digit = len(str(encrypted_block))
                            max_digit = max(max_digit, current_digit)
                            ciphertext.append(encrypted_block)

                # Convert ASCII values to Base64 encoded strings
                base64_ciphertext = [
                    base64.b64encode(str(block).encode()).decode()
                    for block in ciphertext
                ]

                # Simpan hasil enkripsi ke dalam file teks
                if output_path.strip() != "":
                    # Save the Base64-encoded result to a text file
                    with open(output_path, "w") as base64_file:
                        base64_file.write(" ".join(base64_ciphertext))
                        st.success("Sukses! Hasil enkripsi tersimpan")
                        # Save the Base64-encoded result to a separate file
                        base64_content = " ".join(base64_ciphertext)
                        # save_base64_to_text(base64_content, output_path + "_base64.txt")

                        # Create a download link for the original file
                        download_link = create_download_link(
                            base64_content, output_path
                        )

                        # Display the download link
                        st.markdown(download_link, unsafe_allow_html=True)

                    # Menyimpan hasil encoding Base64 ke dalam file teks (opsional)
                else:
                    st.warning(
                        "Silakan masukkan nama file untuk menyimpan hasil enkripsi."
                    )
            else:
                st.warning("Silakan pilih file untuk dienkripsi.")

            return max_digit

        def decryption_menu(max_digit):
            st.title("RSA Decryption")

            n = st.number_input(
                "Masukan nilai n:", min_value=1, step=1, value=1, key="decryption_n"
            )
            d = st.number_input(
                "Masukan kunci private d:",
                min_value=1,
                step=1,
                value=1,
                key="decryption_d",
            )
            input_file = st.file_uploader("Pilih file untuk didekripsi", type=["txt"])
            process_path = st.text_input(
                "Masukkan path untuk menyimpan process dekripsi (contoh process_dekripsi.txt):"
            )
            output_path = st.text_input(
                "Masukkan nama file untuk menyimpan hasil dekripsi (contoh: hasil_dekripsi.txt):"
            )

            if input_file is not None:
                # Read the content of the uploaded file line by line
                lines = input_file.getvalue().decode("utf-8").splitlines()

                # Convert each line to a list of integers
                ciphertext_str = " ".join(lines)
                try:
                    # Convert Base64-encoded strings back to integers
                    ciphertext_blocks = [
                        int(base64.b64decode(block).decode())
                        for block in ciphertext_str.split()
                    ]
                except ValueError as e:
                    st.error(f"Failed to convert content to a list of integers. {e}")
                    return

                decrypted_message = ""
                values = []

                if process_path.strip() != "":
                    # Open the file in append mode
                    with open(process_path, "a") as base64_file:
                        # Iterate through each block in the ciphertext
                        for block in ciphertext_blocks:
                            decrypted_block = pow(block, d, n)
                            decrypted_char = chr(
                                decrypted_block
                            )  # Convert ASCII value to character

                            # Append the value to the list
                            values.append(decrypted_block)

                            # Write the details of the current block to the file
                            base64_file.write(
                                f"{block}^{d} mod {n} is {decrypted_block} which is '{decrypted_char}'\n"
                            )

                            decrypted_message += decrypted_char

                # Simpan hasil dekripsi ke dalam file teks
                if output_path.strip() != "":
                    # Save the Base64-encoded result to a text file
                    with open(output_path, "w") as base64_file:
                        base64_file.write(decrypted_message)
                        st.success("Sukses! Hasil dekripsi tersimpan")

                    # Create a download link for the decrypted file
                    download_link = create_download_link(decrypted_message, output_path)

                    # Display the download link
                    st.markdown(download_link, unsafe_allow_html=True)

                else:
                    st.warning(
                        "Silakan masukkan nama file untuk menyimpan hasil dekripsi."
                    )
            else:
                st.warning("Silakan pilih file untuk didekripsi.")

        # Fungsi untuk menghitung totient n dari dua bilangan prima p dan q
        def calculate_totient(p, q):
            return (p - 1) * (q - 1)

        # Fungsi untuk mencari bilangan prima yang relatif prima terhadap totient n
        def generate_coprime(num_digits, totient_n):
            while True:
                random_prime = generate_random_prime(num_digits)
                if math.gcd(random_prime, totient_n) == 1:
                    return random_prime

        # Fungsi untuk mengenerate bilangan prima dengan jumlah digit yang diinginkan
        def generate_random_prime(num_digits):
            min_value = 10 ** (num_digits - 1)
            max_value = (10**num_digits) - 1

            while True:
                random_prime = random.randint(min_value, max_value)
                if is_prime(random_prime):
                    return random_prime

        # Fungsi untuk menampilkan menu bilangan prima custom dalam Streamlit
        def custom_prime_menu():
            st.header("Custom Prime Numbers Menu")

            # Masukkan jumlah digit bilangan prima yang diinginkan
            num_digits = st.number_input(
                "Masukkan jumlah digit bilangan prima yang diinginkan:",
                min_value=1,
                step=1,
            )

            # Tombol untuk generate bilangan prima
            if st.button("Generate Prime Numbers"):
                # Generate bilangan prima dengan jumlah digit yang diinginkan
                prime1 = generate_random_prime(int(num_digits))
                prime2 = generate_random_prime(int(num_digits))

                if prime1 is not None and prime2 is not None:
                    st.write(f"Bilangan prima dengan {num_digits} digit (p): {prime1}")
                    st.write(f"Bilangan prima dengan {num_digits} digit (q): {prime2}")
                    totient_n = calculate_totient(prime1, prime2)
                    e = generate_coprime(int(num_digits), totient_n)

                    st.write(f"Totient n: {totient_n}")
                    st.write(
                        f"Bilangan prima relatif prima terhadap totient n (e): {e}"
                    )
                else:
                    st.write(f"Tidak ada bilangan prima dengan {num_digits} digit")

        choice = st.sidebar.selectbox(
            "Select an option",
            ["Make keys", "Encryption", "Decryption", "Custom Prime", "Exit"],
        )

        if choice == "Make keys":
            make_key()
        elif choice == "Encryption":
            max_digit = encryption_menu()
        elif choice == "Decryption":
            max_digit = st.number_input(
                "Enter max digit:", value=3, min_value=1, max_value=10, step=1
            )
            decryption_menu(max_digit)
        elif choice == "Custom Prime":
            custom_prime_menu()
        elif choice == "Exit":
            st.balloons()
            st.success("Terima Kasih Telah Berkunjung Semoga Harimu Menyenangkan")
            st.stop()


if __name__ == "__main__":
    main()
