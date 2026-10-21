"""Names and element-pair yoga tables documented by Edward Henning (2007).

Source: Kālacakra and the Tibetan Calendar, owner-supplied PDF,
Chapter IV printed pp203–204, Appendix I printed pp356–362.
Source-page-transcribed labels; they do not imply auspicious results,
medical effects, or human predictive validity.

Three DIFFERENT uses of "yoga" remain separate:
- 10 unordered weekday-element + lunar mansion-element combinations
- 27 angle-sum yoga types with Phugpa/Tsurphu NAME shift
- another 28 weekday-mansion conjunctions ('phrod 'byor), for which a
  complete mapping is NOT provided here.
Tibetan and Indian 27-mansion lists differ at 21 (Śravaṇa vs Abhijit).
"""
from __future__ import annotations
from dataclasses import dataclass

WEEKDAY_NAMES=("Saturday","Sunday","Monday","Tuesday","Wednesday",
               "Thursday","Friday")
WEEKDAY_ELEMENTS=("earth","fire","water","fire","water","wind","earth")
MANSION_TIBETAN_27=(
  "Aśvinī","Bharanī","Kṛttikā","Rohiṇī","Mṛgaśiras","Ārdrā",
  "Punarvasu","Puṣya","Āśleṣā","Maghā","Pūrvaphalgunī",
  "Uttaraphalgunī","Hasta","Citrā","Svātī","Viśākhā",
  "Anurādhā","Jyeṣṭhā","Mūla","Pūrvāṣāḍhā","Uttarāṣāḍhā",
  "Śravaṇa","Dhaniṣṭhā","Śatabhiṣaj","Pūrvabhādrapadā",
  "Uttarabhādrapadā","Revatī"
)
MANSION_ELEMENTS_27=(
 "wind","fire","fire","earth","wind","water","wind",
 "fire","water","fire","fire","wind","wind","wind",
 "wind","wind","earth","earth","water","water",
 "earth","earth","water","earth","fire","water","water"
)
ANGULAR_YOGA_PHUGPA_27=(
 "Viṣkambha","Prīti","Āyuṣmat","Saubhāgya","Śobhana",
 "Atigaṇḍa","Sukarman","Dhṛti","Śūla","Gaṇḍa","Vṛddhi",
 "Dhruva","Vyāghāta","Harṣaṇa","Vajra","Siddhi",
 "Vyatīpāta","Varīyas","Parigha","Śiva","Siddha",
 "Sādhya","Śubha","Śukla","Brahman","Indra","Vaidhṛti"
)
CHANGING_KARANA_7=(
 "Vava","Valava","Kaulava","Taitila","Gara","Vaṇija","Viṣṭi"
)
FIXED_KARANA_BY_H={1:"Kintughna",58:"Śakuni",
                   59:"Catuṣpada",60:"Nāga"}
# Normalize each unordered pair by lexical sorting. This covers exactly
# all 10 multisets of size 2 over earth/fire/water/wind.
_ELEMENTAL_YOGA_SOURCE_PAIRS=(
 ("earth","earth","Siddhi"),
 ("water","water","Amṛta"),
 ("earth","water","Yauvana"),
 ("fire","fire","Pragati"),
 ("wind","wind","Sampanna"),
 ("fire","wind","Balayukta"),
 ("earth","wind","Alābha"),
 ("water","wind","Pratikūla"),
 ("earth","fire","Dahana"),
 ("fire","water","Maraṇa"),
)
ELEMENTAL_YOGAS={
 tuple(sorted((e1,e2))):name for e1,e2,name in _ELEMENTAL_YOGA_SOURCE_PAIRS
}
assert len(ELEMENTAL_YOGAS)==10
assert len(MANSION_TIBETAN_27)==len(MANSION_ELEMENTS_27)==27
assert len(ANGULAR_YOGA_PHUGPA_27)==27


def _n(i: object, size: int, label: str) -> int:
 if type(i) is not int or not 0<=i<size:
  raise ValueError(f"{label}: expected zero-based integer in [0,{size})")
 return i


def mansion_name(i: int, *, name_tradition: str) -> str:
 """Mansion 21 differs: Tibet Śravaṇa, Indian convention Abhijit."""
 _n(i,27,"mansion index")
 if name_tradition not in ("tibetan_27","indian_27"):
  raise ValueError("Select source name tradition explicitly")
 if name_tradition=="indian_27" and i==21:
  return "Abhijit"
 return MANSION_TIBETAN_27[i]


def angular_yoga_name(i:int,*,calendar_policy:str)->str:
 """Henning App I: Phugpa yoga0 Viṣkambha, Tsurphu yoga0 Vaidhṛti."""
 _n(i,27,"angular yoga index")
 if calendar_policy=="phugpa":
  return ANGULAR_YOGA_PHUGPA_27[i]
 if calendar_policy=="tsurphu":
  return ANGULAR_YOGA_PHUGPA_27[(i-1)%27]
 raise ValueError("Select phugpa or tsurphu names explicitly")


def elemental_yoga_name(weekday_index:int,mansion_index:int)->str:
 """Ten weekday-element/mansion-element yogas (not 27 angular yogas)."""
 a=WEEKDAY_ELEMENTS[_n(weekday_index,7,"weekday")]
 b=MANSION_ELEMENTS_27[_n(mansion_index,27,"mansion")]
 return ELEMENTAL_YOGAS[tuple(sorted((a,b)))]


def karana_name_at_H(H:int)->str:
 """Karaṇa 1..60, Henning Appendix I and Janson §10(viii)."""
 if type(H) is not int or not 1<=H<=60:
  raise ValueError("half lunar day position must be 1–60 integer")
 if H in FIXED_KARANA_BY_H:
  return FIXED_KARANA_BY_H[H]
 return CHANGING_KARANA_7[(H-2)%7]


def karana_names_for_tithi(day:int)->tuple[str,str]:
 if type(day) is not int or not 1<=day<=30:
  raise ValueError("tithi must be 1–30")
 return karana_name_at_H(2*day-1),karana_name_at_H(2*day)


@dataclass(frozen=True)
class NamedDay:
 """Names sourced from Henning, numeric almanac from Janson."""
 weekday: str
 weekday_element: str
 mansion: str
 mansion_element: str
 elemental_yoga_10: str
 angular_yoga_27: str
 karana_at_dawn: str|None
 unknown_other_weekday_mansion_yoga_28: None = None


def named_day(almanac:object,*,name_tradition:str)->NamedDay|None:
 """A non-skipped T58 model-day -> Henning source titles.
 Karaṇa dawn name only if T58 explicit Henning equal duration was supplied.
 """
 if getattr(almanac,"skipped"):
  return None
 w=getattr(almanac,"weekday_number")
 m=getattr(almanac,"mansion_index_0_to_26")
 y=getattr(almanac,"yoga_index_0_to_26")
 policy=getattr(almanac,"system")
 if w is None or m is None or y is None:
  raise ValueError("Calendar-day attributes must be known")
 x=getattr(almanac,"karana_at_dawn_id")
 karana=None
 if x is not None:
  if x.startswith("fixed_"):
   karana=karana_name_at_H(int(x.split("_")[1]))
  elif x.startswith("changing_"):
   karana=CHANGING_KARANA_7[int(x.split("_")[1])-1]
  else:
   raise ValueError("Unrecognized explicit T58 karaṇa ID")
 return NamedDay(
  weekday=WEEKDAY_NAMES[_n(w,7,"weekday")],
  weekday_element=WEEKDAY_ELEMENTS[_n(w,7,"weekday")],
  mansion=mansion_name(m,name_tradition=name_tradition),
  mansion_element=MANSION_ELEMENTS_27[_n(m,27,"mansion")],
  elemental_yoga_10=elemental_yoga_name(w,m),
  angular_yoga_27=angular_yoga_name(y,calendar_policy=policy),
  karana_at_dawn=karana
 )
