
import gc
import sys
import time
import weakref
import tracemalloc


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


class Node:
    """A tiny object that announces when it is destroyed."""

    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"   [__del__] {self.name} destroyed")


# EXPERIMENT 1: Reference Counting
def exp1_reference_counting():
    section("1. Reference counting: instant cleanup")

    a = Node("A")
    print("refcount of A:", sys.getrefcount(a))

    b = a
    print("after b = a, refcount:", sys.getrefcount(a))

    del a
    print("after del a, refcount:", sys.getrefcount(b))

    print("deleting the last name...")
    del b
    print("(destroyed immediately, no gc needed)")


# EXPERIMENT 2: Reference Cycle
def exp2_cycle_and_manual_collect():
    section("2. Reference cycle until gc.collect()")

    gc.collect()
    gc.disable()

    print("gc enabled?", gc.isenabled())

    x, y = Node("X"), Node("Y")
    x.other, y.other = y, x

    del x, y

    print("deleted both names. Nothing printed => still in memory")

    found = gc.collect()
    print(f"gc.collect() returned {found}")

    gc.enable()


# EXPERIMENT 3: Thresholds and Statistics
def exp3_thresholds_counts_stats():
    section("3. Thresholds, counts and statistics")

    print("get_threshold():", gc.get_threshold())
    print("get_count():", gc.get_count())

    s = gc.get_stats()[0]

    print("collections =", s["collections"])
    print("collected =", s["collected"])
    print("uncollectable =", s["uncollectable"])


# EXPERIMENT 4: Automatic Collection
def exp4_automatic_trigger():
    section("4. Automatic collection")

    events = []

    def watcher(phase, info):
        if phase == "stop":
            events.append(
                (info["generation"], info["collected"])
            )

    gc.callbacks.append(watcher)

    old = gc.get_threshold()
    gc.collect()

    gc.set_threshold(50, 5, 5)
    events.clear()

    for _ in range(300):
        a, b = [], []
        a.append(b)
        b.append(a)

    gc.set_threshold(*old)
    gc.callbacks.remove(watcher)

    print(f"GC ran {len(events)} times by itself.")
    print("First few runs:", events[:5])


# EXPERIMENT 5: Generations
def exp5_generations():
    section("5. Generations")

    gc.collect()

    keeper = [Node("K")]
    keeper[0].other = keeper

    print("Before collect(0):",
          [len(gc.get_objects(g)) for g in range(3)])

    gc.collect(0)

    print("After collect(0):",
          [len(gc.get_objects(g)) for g in range(3)])

    gc.collect(1)

    print("After collect(1):",
          [len(gc.get_objects(g)) for g in range(3)])

    print("Young objects move to older generations")

    keeper[0].other = None
    del keeper


# EXPERIMENT 6: Memory Effect
def exp6_memory_effect():
    section("6. Memory effect of cycles")

    gc.collect()
    gc.disable()

    tracemalloc.start()

    base = tracemalloc.get_traced_memory()[0]

    for _ in range(20000):
        a, b = {}, {}
        a["b"], b["a"] = b, a

    del a, b

    leaked = tracemalloc.get_traced_memory()[0] - base

    n = gc.collect()

    after = tracemalloc.get_traced_memory()[0] - base

    tracemalloc.stop()
    gc.enable()

    print(f"Memory held: {leaked / 1024:.1f} KiB")
    print(f"Objects freed: {n}")
    print(f"Memory after collect: {after / 1024:.1f} KiB")


# EXPERIMENT 7: DEBUG_SAVEALL
def exp7_debug_saveall():
    section("7. DEBUG_SAVEALL")

    gc.collect()

    gc.set_debug(gc.DEBUG_SAVEALL)

    p, q = [1], [2]

    p.append(q)
    q.append(p)

    del p, q

    gc.collect()

    print("gc.garbage:", gc.garbage)

    gc.set_debug(0)
    gc.garbage.clear()

    gc.collect()


# EXPERIMENT 8: Tracking and Weak References
def exp8_tracking_and_weakref():
    section("8. is_tracked() and weak references")

    samples = [
        ("int 5", 5),
        ("string", "hi"),
        ("list", [1]),
        ("empty dict", {}),
        ("dict with list", {"k": [1]}),
        ("tuple of ints", (1, 2)),
        ("Node object", Node("T"))
    ]

    for label, obj in samples:
        print(
            f"{label:<16} tracked by gc? {gc.is_tracked(obj)}"
        )

    n = Node("W")

    ref = weakref.ref(n)

    print("weakref alive?", ref() is not None)

    del n

    print("after del, weakref alive?", ref() is not None)


# EXPERIMENT 9: Freeze
def exp9_freeze():
    section("9. gc.freeze()")

    gc.collect()

    print("frozen before:", gc.get_freeze_count())

    gc.freeze()

    print("frozen after:", gc.get_freeze_count())

    gc.unfreeze()

    print("after unfreeze:", gc.get_freeze_count())


# EXPERIMENT 10: Timing
def exp10_timing():
    section("10. Cost of automatic GC")

    def work():
        data = []

        for i in range(400000):
            data.append([i])

        return len(data)

    results = {}

    for label, enabled in (
        ("gc enabled", True),
        ("gc disabled", False)
    ):
        gc.collect()

        (gc.enable if enabled else gc.disable)()

        t = time.perf_counter()

        work()

        results[label] = time.perf_counter() - t

        gc.enable()

        print(f"{label}: {results[label] * 1000:.1f} ms")

    print("Timings vary by machine and Python version.")


# MAIN PROGRAM
if __name__ == "__main__":

    print("Python", sys.version.split()[0])

    exp1_reference_counting()
    exp2_cycle_and_manual_collect()
    exp3_thresholds_counts_stats()
    exp4_automatic_trigger()
    exp5_generations()
    exp6_memory_effect()
    exp7_debug_saveall()
    exp8_tracking_and_weakref()
    exp9_freeze()
    exp10_timing()
