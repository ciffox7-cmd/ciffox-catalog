from typing import List, Dict, Optional
from rapidfuzz import fuzz, process


def _best_match(name: Optional[str], rate_rows: List[Dict]) -> Dict:
	if not name:
		return {"matched": False}
	choices = [(r.get("raw") or " ", r) for r in rate_rows]
	if not choices:
		return {"matched": False}
	best = process.extractOne(name, [c[0] for c in choices], scorer=fuzz.WRatio)
	if not best:
		return {"matched": False}
	score, idx = best[1], best[2]
	row = choices[idx][1]
	return {"matched": score >= 70, "score": score, "rate_row": row}


def match_products_with_rates(products: List[Dict], rates: List[Dict]) -> List[Dict]:
	matched: List[Dict] = []
	for p in products:
		res = _best_match(p.get("name"), rates)
		combined = {**p, **res}
		matched.append(combined)
	return matched


