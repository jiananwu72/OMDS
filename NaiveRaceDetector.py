from collections import defaultdict

class NaiveRaceDetector:
    def __init__(self):
        # Dictionary to store the trace of accesses per variable.
        # Format: { variable: [(thread_id, access_type, event_index), ...] }
        self.access_log = defaultdict(list)
        self.event_counter = 0  # Global timestamp for ordering accesses.

    def log_access(self, thread_id, variable, access_type):
        """
        Log a memory access.
        access_type should be either 'read' or 'write'.
        """
        self.event_counter += 1
        self.access_log[variable].append((thread_id, access_type, self.event_counter))

    def detect_races(self):
        """
        Naively scan through the access log for potential races.
        A race is reported if two accesses to the same variable come from different
        threads, at least one of the accesses is a write, and they are not ordered
        by any synchronization (this simplified example does not handle synchronization).
        """
        races = []
        for var, accesses in self.access_log.items():
            n = len(accesses)
            for i in range(n):
                for j in range(i + 1, n):
                    tid1, type1, t1 = accesses[i]
                    tid2, type2, t2 = accesses[j]
                    if tid1 != tid2:
                        # If either access is a write, flag a potential race.
                        if type1 == 'write' or type2 == 'write':
                            races.append((var, accesses[i], accesses[j]))
        return races

# Example usage:
if __name__ == "__main__":
    detector = NaiveRaceDetector()
    
    # Simulate some memory accesses on a shared variable "x".
    detector.log_access("Thread-A", "x", "read")
    detector.log_access("Thread-B", "x", "write")
    detector.log_access("Thread-A", "x", "write")
    detector.log_access("Thread-B", "x", "read")
    
    potential_races = detector.detect_races()
    if potential_races:
        print("Potential Data Races Detected:")
        for race in potential_races:
            var, access1, access2 = race
            print(f"Variable {var}: {access1} <--> {access2}")
    else:
        print("No races detected.")
