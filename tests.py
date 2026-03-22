from main import BooksCollector
import pytest

class TestBooksCollector:

    @pytest.mark.parametrize("book_name, is_valid", [
        ("Короткий заголовок", True),
        ("a" * 40, True),
        ("a" * 41, False),
        ("", False),
    ])
    def test_add_new_book_valid_and_invalid_names(self, collector, book_name, is_valid):
        collector.add_new_book(book_name)
        if is_valid:
            assert book_name in collector.get_books_genre()
        else:
            assert book_name not in collector.get_books_genre()

    def test_add_new_book_duplicate(self, collector):
        book_name = "Дубликат"
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == 1


    def test_set_book_genre_valid_case(self, collector):
        collector.add_new_book("Вархаммер")
        collector.set_book_genre("Вархаммер", "Фантастика")
        assert collector.get_book_genre("Вархаммер") == "Фантастика"

    def test_set_book_genre_book_not_found(self, collector):
        collector.set_book_genre("Нет в коллекции", "Фантастика")
        assert collector.get_book_genre("Нет в коллекции") is None

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book("Варкрафт")
        collector.set_book_genre("Варкрафт", "Неизвестный жанр")
        assert collector.get_book_genre("Варкрафт") == ""


    def test_get_book_genre_existing_book_with_genre(self, collector):
        book_name = "Гремлины"
        genre = "Ужасы"
        collector.add_new_book(book_name)
        collector.books_genre[book_name] = genre
        result = collector.get_book_genre(book_name)
        assert result == genre

    def test_get_book_genre_existing_book_without_genre(self, collector):
        collector.add_new_book("Без жанра")
        assert collector.get_book_genre("Без жанра") == ""

    def test_get_book_genre_nonexistent_book(self, collector):
        assert collector.get_book_genre("Нет в коллекции") is None


    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Грань будущего", "Интерстеллар"]),
        ("Ужасы", ["Зубастики"]),
        ("Неизвестный жанр", []),
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected_books):
        books_by_genre = {
            "Фантастика": ["Грань будущего", "Интерстеллар"],
            "Ужасы": ["Зубастики"],
        }
        for genre_name, books in books_by_genre.items():
            for book in books:
                collector.add_new_book(book)
                collector.set_book_genre(book, genre_name)
        result = collector.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(expected_books)


    def test_get_books_genre(self, collector):
        collector.add_new_book("Первому игроку приготовиться")
        collector.set_book_genre("Первому игроку приготовиться", "Фантастика")
        collector.add_new_book("Аватар")
        expected = {
            "Первому игроку приготовиться": "Фантастика",
            "Аватар": ""
        }
        assert collector.get_books_genre() == expected


    def test_get_books_for_children(self, collector):
        books_data = [
            ("Пила", "Ужасы"),
            ("Король Лев", "Мультфильмы"),
            ("Один Дома", "Комедии"),
        ]
        for book, genre in books_data:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
        result = collector.get_books_for_children()
        assert "Король Лев" in result
        assert "Один Дома" in result
        assert "Пила" not in result


    def test_add_book_in_favorites_valid_book(self, collector):
        collector.add_new_book("Одержимость")
        collector.add_book_in_favorites("Одержимость")
        assert "Одержимость" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_book_not_in_collection(self, collector):
        collector.add_book_in_favorites("Книга не в коллекции")
        assert "Книга не в коллекции" not in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book("Пожизненно")
        collector.add_book_in_favorites("Пожизненно")
        collector.add_book_in_favorites("Пожизненно")
        assert len(collector.get_list_of_favorites_books()) == 1


    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Рокки")
        collector.add_book_in_favorites("Рокки")
        collector.delete_book_from_favorites("Рокки")
        assert "Рокки" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_book_not_in_favorites(self, collector):
        collector.delete_book_from_favorites("Нет в избранном")
        assert "Нет в избранном" not in collector.get_list_of_favorites_books()


    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Назад в Будущее")
        collector.add_new_book("Бесконечная История")

        collector.favorites = ["Назад в Будущее"]
        
        favorites = collector.get_list_of_favorites_books()
        assert "Назад в Будущее" in favorites
        assert "Бесконечная История" not in favorites
        assert len(favorites) == 1