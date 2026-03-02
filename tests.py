from main import BooksCollector
import pytest

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    @pytest.mark.parametrize("book_name, is_valid", [
        ("Короткий заголовок", True),
        ("a" * 40, True),
        ("a" * 41, False),
        ("", False),
        ("   ", False),
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
        collector.add_new_book("Гремлины")
        collector.set_book_genre("Гремлины", "Ужасы")
        assert collector.get_book_genre("Гремлины") == "Ужасы"

    def test_get_book_genre_existing_book_without_genre(self, collector):
        collector.add_new_book("Без жанра")
        assert collector.get_book_genre("Без жанра") == ""

    def test_get_book_genre_nonexistent_book(self, collector):
        assert collector.get_book_genre("Нет в коллекции") is None