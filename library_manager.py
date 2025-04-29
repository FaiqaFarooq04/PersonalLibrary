import streamlit as st
import os

# File Handling Functions
def load_library_txt():
    library = []
    if os.path.exists("library.txt"):
        with open("library.txt", "r") as f:
            for line in f:
                title, author, year, genre, status = line.strip().split("|")
                book = {
                    "Title": title,
                    "Author": author,
                    "Publication Year": int(year),
                    "Genre": genre,
                    "Read Status": status == "Read"
                }
                library.append(book)
    return library

def save_library_txt(library):
    with open("library.txt", "w") as f:
        for book in library:
            f.write(f"{book['Title']}|{book['Author']}|{book['Publication Year']}|{book['Genre']}|{'Read' if book['Read Status'] else 'Unread'}\n")# Write each book's information to the file, separated by '|'

# App starts here
st.set_page_config(page_title="Personal Library Manager", page_icon="📚")

st.sidebar.markdown("## 📚 Welcome to your Personal Library Manager!")
choice = st.sidebar.radio(
    label="",
    options=[
        "1. Add a book",
        "2. Remove a book",
        "3. Search for a book",
        "4. Display all books",
        "5. Display statistics",
        "6. Exit"
    ],
    index=0
)

# Load the library from the .txt file
library = load_library_txt()

# Add Book
st.title("Personal Library")

if choice.startswith("1"):
    st.subheader("➕ Add a Book")

    # Get book details from the user via input fields
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read_status = st.radio("Have you read this book?", ["Yes", "No"],horizontal=True) == "Yes"

    if st.button("Add Book"):
        if not title or not author:
            st.warning("Title and author are required.")
        else:
            book = {
                "Title": title,
                "Author": author,
                "Publication Year": int(year),
                "Genre": genre,
                "Read Status": read_status
            }
            library.append(book)
            save_library_txt(library)  # Save the updated library to the file
            st.success(f'"{title}" has been added.')

# Remove Book
elif choice.startswith("2"):
    st.subheader("❌ Remove a Book")

    if not library:
        st.info("Library is empty.")
    else:
        # Create a list of book titles for the user to select from
        book_titles = [f'{book["Title"]} by {book["Author"]}' for book in library]
        selected = st.selectbox("Select a book to remove:", book_titles)

        if st.button("Remove Book"):
            for book in library:
                if f'{book["Title"]} by {book["Author"]}' == selected:
                    library.remove(book)
                    save_library_txt(library)  # Save to .txt file
                    st.success(f'"{book["Title"]}" removed.')
                    break

# Search
elif choice.startswith("3"):
    st.subheader("🔍 Search for a Book")

    st.markdown("Search by:\n1. Title\n2. Author")
    search_type = st.text_input("Enter your choice (1 or 2):")

    if search_type.strip() == "1":
        query = st.text_input("Enter the title:")
        if query:
            results = [book for book in library if query.lower() in book["Title"].lower()]
            if results:
                st.subheader("Matching Books:")
                for idx, book in enumerate(results, 1):
                    status = "Read" if book["Read Status"] else "Unread"
                    st.write(f'{idx}. {book["Title"]} by {book["Author"]} ({book["Publication Year"]}) - {book["Genre"]} - {status}')
            else:
                st.info("No matching books found.")

    elif search_type.strip() == "2":
        query = st.text_input("Enter the author's name:")
        if query:
            matched_books = [book for book in library if query.lower() in book["Author"].lower()]
            if matched_books:
                read_books = [b for b in matched_books if b["Read Status"]]
                unread_books = [b for b in matched_books if not b["Read Status"]]

                st.subheader(f"Books by {query.title()}")

                st.markdown("#### ✅ Read Books")
                if read_books:
                    for book in read_books:
                        st.markdown(f"**{book['Title']}** ({book['Publication Year']}) - {book['Genre']}")
                else:
                    st.write("No read books.")

                st.markdown("#### 📖 Unread Books")
                if unread_books:
                    for book in unread_books:
                        st.markdown(f"**{book['Title']}** ({book['Publication Year']}) - {book['Genre']}")
                else:
                    st.write("No unread books.")
            else:
                st.info("No books found by this author.")
    else:
        st.info("Enter 1 or 2 to search by Title or Author.")

# Display All Books
elif choice.startswith("4"):
    st.subheader("📚 All Books")

    if library:
        read_books = [book for book in library if book["Read Status"]]
        unread_books = [book for book in library if not book["Read Status"]]

        st.markdown("### ✅ Read Books")
        if read_books:
            for book in read_books:
                st.markdown(f"**Title:** {book['Title']}")
                st.markdown(f"**Author:** {book['Author']}")
                st.markdown(f"**Year:** {book['Publication Year']}")
                st.markdown(f"**Genre:** {book['Genre']}")
                st.markdown("---")
        else:
            st.info("No books marked as read.")

        st.markdown("### 📖 Unread Books")
        if unread_books:
            for book in unread_books:
                st.markdown(f"**Title:** {book['Title']}")
                st.markdown(f"**Author:** {book['Author']}")
                st.markdown(f"**Year:** {book['Publication Year']}")
                st.markdown(f"**Genre:** {book['Genre']}")
                st.markdown("---")
        else:
            st.info("No unread books.")
    else:
        st.info("Library is empty.")

# Display Statistics
elif choice.startswith("5"):
    st.subheader("📊 Statistics")

    total = len(library)
    read = sum(book["Read Status"] for book in library)
    percent = (read / total * 100) if total > 0 else 0
    st.write(f"📘 Total books: {total}")
    st.write(f"✅ Books read: {read}")
    st.write(f"📈 Percentage read: {percent:.2f}%")

# Exit
elif choice.startswith("6"):
    st.success("Thanks for using Personal Library Manager! 👋")