"""Tests for the DataFrame utility."""

from cacao.server.data import DataFrame


class TestDataFrame:
    def test_from_records(self) -> None:
        df = DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        assert len(df) == 2
        assert df.columns == ["a", "b"]

    def test_from_columnar_dict(self) -> None:
        df = DataFrame({"x": [10, 20], "y": [30, 40]})
        assert len(df) == 2
        assert df[0] == {"x": 10, "y": 30}

    def test_getitem_column(self) -> None:
        df = DataFrame([{"name": "Alice"}, {"name": "Bob"}])
        assert df["name"] == ["Alice", "Bob"]

    def test_getitem_index(self) -> None:
        df = DataFrame([{"v": 1}, {"v": 2}, {"v": 3}])
        assert df[1] == {"v": 2}

    def test_filter(self) -> None:
        df = DataFrame([{"age": 15}, {"age": 25}, {"age": 10}])
        result = df.filter(lambda r: r["age"] >= 18)
        assert len(result) == 1
        assert result[0]["age"] == 25

    def test_select(self) -> None:
        df = DataFrame([{"a": 1, "b": 2, "c": 3}])
        result = df.select("a", "c")
        assert result[0] == {"a": 1, "c": 3}

    def test_sort(self) -> None:
        df = DataFrame([{"n": 3}, {"n": 1}, {"n": 2}])
        result = df.sort("n")
        assert [r["n"] for r in result] == [1, 2, 3]

    def test_sort_reverse(self) -> None:
        df = DataFrame([{"n": 1}, {"n": 3}, {"n": 2}])
        result = df.sort("n", reverse=True)
        assert [r["n"] for r in result] == [3, 2, 1]

    def test_limit_and_head(self) -> None:
        df = DataFrame([{"i": i} for i in range(10)])
        assert len(df.limit(3)) == 3
        assert len(df.head(2)) == 2

    def test_tail(self) -> None:
        df = DataFrame([{"i": i} for i in range(10)])
        result = df.tail(3)
        assert [r["i"] for r in result] == [7, 8, 9]

    def test_map_column(self) -> None:
        df = DataFrame([{"price": 10}, {"price": 20}])
        result = df.map("price", lambda x: x * 2)
        assert [r["price"] for r in result] == [20, 40]

    def test_add_column(self) -> None:
        df = DataFrame([{"a": 2, "b": 3}])
        result = df.add_column("c", lambda r: r["a"] * r["b"])
        assert result[0]["c"] == 6

    def test_group_by(self) -> None:
        df = DataFrame([
            {"cat": "A", "v": 1},
            {"cat": "B", "v": 2},
            {"cat": "A", "v": 3},
        ])
        groups = df.group_by("cat")
        assert len(groups["A"]) == 2
        assert len(groups["B"]) == 1

    def test_aggregate(self) -> None:
        df = DataFrame([{"v": 10}, {"v": 20}, {"v": 30}])
        result = df.aggregate(total=lambda rows: sum(r["v"] for r in rows))
        assert result["total"] == 60

    def test_unique(self) -> None:
        df = DataFrame([{"c": "a"}, {"c": "b"}, {"c": "a"}])
        assert set(df.unique("c")) == {"a", "b"}

    def test_sum_mean_min_max(self) -> None:
        df = DataFrame([{"v": 10}, {"v": 20}, {"v": 30}])
        assert df.sum("v") == 60.0
        assert df.mean("v") == 20.0
        assert df.min("v") == 10
        assert df.max("v") == 30

    def test_to_dict_records(self) -> None:
        data = [{"a": 1}, {"a": 2}]
        df = DataFrame(data)
        assert df.to_dict("records") == data

    def test_to_dict_list(self) -> None:
        df = DataFrame([{"x": 1, "y": 2}, {"x": 3, "y": 4}])
        result = df.to_dict("list")
        assert result == {"x": [1, 3], "y": [2, 4]}

    def test_empty(self) -> None:
        df = DataFrame([])
        assert len(df) == 0
        assert df.columns == []
        assert df.mean("x") == 0
        assert df.min("x") is None
