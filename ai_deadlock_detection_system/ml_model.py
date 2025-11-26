try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
except Exception:
    np = None
    RandomForestClassifier = None


class DeadlockMLModel:

    def __init__(self):
        # If scikit-learn is available, build a small demo model.
        if RandomForestClassifier is not None and np is not None:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            X = np.array([
                [2,3,1],
                [5,1,0],
                [7,3,2],
                [1,1,0],
                [9,5,3],
                [4,4,2],
                [6,2,1]
            ])
            y = np.array([1,0,1,0,1,0,1])
            try:
                self.model.fit(X, y)
            except Exception:
                # fallback to rule-based if training fails
                self.model = None
        else:
            # No heavy ML libraries available — use a lightweight heuristic fallback.
            self.model = None

    def predict(self, features):
        # If we have a trained sklearn model, use it.
        if self.model is not None:
            try:
                prob = float(self.model.predict_proba([features])[0][1])
                cls = int(prob > 0.5)
                return prob, cls
            except Exception:
                pass

        # Heuristic fallback: use simple rules to estimate deadlock probability.
        # Features expected: [processes, resources, hold_count]
        try:
            p = int(features[0]) if len(features) > 0 else 0
            r = int(features[1]) if len(features) > 1 else 0
            h = int(features[2]) if len(features) > 2 else 0
        except Exception:
            p, r, h = 0, 0, 0

        # Basic heuristic: more processes than resources and higher hold_count increase deadlock risk
        score = 0.0
        if r > 0:
            score += max(0.0, (p - r) / max(1, r)) * 0.6
        score += min(h / 10.0, 1.0) * 0.4

        prob = float(min(max(score, 0.0), 1.0))
        cls = int(prob > 0.5)
        return prob, cls
