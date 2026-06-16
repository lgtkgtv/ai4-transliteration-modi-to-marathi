# The Modi Script: A Stakeholder Tutorial

**Project:** मोडी ते मराठी (modi-to-Marathi)
**Repository:** https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi
**Author:** Sachin · **Purpose:** Give everyone on the project a shared, accurate understanding of the script we are working to preserve.

> This tutorial is written for a general audience but sourced from scholarly and primary references (listed at the end). Where experts on our team know more, please correct and extend it.

---

## 1. Modi in one minute

**Modi (मोडी)** is a cursive script that was used to write the **Marathi** language for centuries — most famously as the official administrative script of the Maratha world from roughly the 17th century until the mid-20th century. It was designed for **speed**: scribes could write it quickly, with few pen-lifts, which made it ideal for letters, accounts, and government records.

| Fact | Detail |
|---|---|
| Script type | Abugida (alphasyllabary) — consonants carry a built-in vowel |
| Writes | Mainly Marathi; occasionally Konkani, Hindi, Gujarati, Sanskrit and others |
| Direction | Left to right |
| Family | Nāgari family — a flowing, "broken" cursive cousin of Devanagari |
| Core letters | ~46 (about 36 consonants + 10 vowels); counts vary by source and period |
| Oldest dated document | 1389 CE, preserved at the Bharat Itihas Sanshodhak Mandal (BISM), Pune |
| Status today | Replaced by Devanagari (Balbodh) for Marathi; very few can read it now |
| Unicode | Block U+11600–U+1165F, added in Unicode 7.0 (June 2014) |

---

## 2. Where the name and the script come from

The name **"Modi"** is widely thought to come from the Marathi verb *moḍaṇe* (मोडणे), "to bend or break" — a fitting description, because many Modi letters look like **"broken," rounded versions of Devanagari letters**, reshaped so the pen need not lift between them.

The script's creation is traditionally attributed to **Hemādpant** (Hemādri), a minister of the **Yādava dynasty** in the late 13th century (during the reigns of Mahādeva, c. 1261–1271, and Rāmachandra, 1271–1309). One traditional account even says he brought the script to India from Sri Lanka. Scholars treat these as traditions rather than settled fact — there are **two main origin theories**, one placing Modi's beginnings around the 12th–13th century and another around the 16th–17th century. What's clear is that Modi was a deliberate adaptation of the **Balbodh** style of Devanagari into a fast, connected hand.

---

## 3. The eras of Modi (the heart of this tutorial)

Modi changed shape over time, and scholars name its phases after the ruling power of each period. The standard classification has **six eras**. Note that some sources group them differently (e.g., collapsing them into four, or adding a "Shahukalin" phase) — the boundaries are scholarly conventions, not hard lines.

| Era | Period | Context | What changed |
|---|---|---|---|
| **Adyakalin** (आद्यकालीन) | 12th c. | Proto-Modi | Earliest, formative shapes |
| **Yadavakalin** (यादवकालीन) | 13th c. | Yādava dynasty | Emerges as a distinct style |
| **Bahamanikalin** (बहमनीकालीन) | 14th–16th c. | Bahmani Sultanate | Influenced by Perso-Arabic writing |
| **Shivakalin** (शिवकालीन) | 17th c. | Reign of Shivaji | The famous **Chitnisi** style develops |
| **Peshwekalin** (पेश्वेकालीन) | 18th – early 19th c. (to 1818) | Maratha Empire / Peshwas | Many sub-styles flourish; more cursive |
| **Anglakalin** (आंग्लकालीन) | 1818 – c. 1952 | British rule | Pen/nib influence; thick–thin strokes; decline |

**The three eras our project focuses on** (following the IIT Roorkee MoDeTrans dataset) are the last three — **Shivakalin, Peshwekalin, and Anglakalin** — for a simple practical reason: well-preserved documents from the earlier Adyakalin and Yadavakalin periods are **scarce**, since so many were lost or damaged. Here is more detail on each of the three.

### 3.1 Shivakalin (शिवकालीन) — 17th century
The era of **Shivaji Maharaj**. Its defining contribution is the **Chitnisi** style, named after **Bālājī Avajī Chitnis**, Shivaji's secretary of state. Chitnisi became the most prominent and standardized way of writing Modi and set the template that later eras built on. Much pre-Shivaji correspondence already existed in Modi; under Shivaji it became firmly established for statecraft.

### 3.2 Peshwekalin (पेश्वेकालीन) — 18th to early 19th century
The high point of Modi, under the **Peshwas** of the Maratha Empire, lasting until **1818**. Writing became **more cursive**, with marked, elongated curves. Several regional/clerical sub-styles flourished side by side:
- **Chitnisi** (the dominant, inherited style)
- **Bilavalkari**
- **Mahadevpanti** (Mahādevpanti)
- **Ranadi**

For our annotators, this means Peshwekalin documents can vary noticeably in "handwriting" even within the same era — something our dataset guidelines must account for.

### 3.3 Anglakalin (आंग्लकालीन) — 1818 to c. 1952
The **British period**, when Modi and English co-existed in the Deccan. The shift from reed to **metal nib pens** introduced **thick-and-thin stroke contrast** for the first time, changing the script's look. Over this period — as printing, standardization, and administrative policy favoured Devanagari — Modi gradually fell out of use, ending around **1952**.

---

## 4. How Modi works as a writing system

Understanding these features explains *why machine transliteration is hard* — every one of them is a challenge for an AI model.

- **Abugida structure.** Each consonant carries an inherent *a* sound. Other vowels are shown with attached signs (*matras*); a special mark (*virama*) removes the inherent vowel. This is the same logic as Devanagari.
- **The headline drawn first.** The horizontal top line (*shirorekha*) is typically drawn **first**, "ruling" the page like lined paper, and then letters are hung beneath it. Crucially, **this line does not break between words** — so Modi text often has **no visible spaces**, and a reader (or model) must infer where words begin and end.
- **Built for continuous writing.** Letters are rounded and "broken" so the pen rarely lifts. Writing Devanagari *ha* can take several pen-lifts; Modi was engineered to avoid them. This is what makes Modi a kind of **shorthand**.
- **Context-sensitive letters and ligatures.** Some consonants keep one fixed shape; others change shape when followed by a vowel; others form ligatures. Special conjuncts (like *ksha*, *tra*) and the letter *ra* behave in particular ways. These context rules make character boundaries ambiguous.
- **Its own numerals.** Modi has distinct digit forms (with their own Unicode points).
- **A script that could double as a cipher.** Because so few outsiders could read it, Modi was sometimes used to keep correspondence private.

---

## 5. What Modi was used for

Modi was the workhorse script of administration and commerce: **land and revenue records, accounts, credit notes (*hundis*), official correspondence, and royal edicts**, as well as religious and scholarly texts. Tens of millions of such documents survive in archives — most famously the **State Archives in Pune** and the **BISM, Pune** — which is exactly why making them machine-readable matters.

---

## 6. The decline — and why the documents are hard to read today

Modi did not vanish on its own; its decline is a documented historical episode (analysed in depth by **Pushkar Sohoni, 2017**). Key threads:

- **Printing favoured Devanagari.** When Marathi printing began, the angular **Balbodh** style of Devanagari was far easier to typeset than flowing Modi. William Carey's first Marathi grammar (1805) was printed in Balbodh simply because Modi type wasn't available to him.
- **Standardization and policy.** Over the 19th–20th centuries, education and administration consolidated around a single Devanagari standard for Marathi.
- **The break in transmission.** Once schools stopped teaching Modi (officially phased out around the **1950s**), each generation had fewer readers. Today only a small number of trained experts can fluently read historical Modi — and many original documents are **faded, brittle, or damaged**.

This combination — *huge volume of documents, tiny number of readers, deteriorating originals* — is the precise gap our project addresses.

---

## 7. Modi in the digital age

- **Unicode.** Modi was encoded in **Unicode 7.0 (June 2014)** at **U+11600–U+1165F**, based on a scholarly encoding proposal by **Anshuman Pandey (2011)**. This is what lets computers store and display Modi consistently.
- **Fonts.** Open Modi fonts now exist — notably **MarathiCursive** and **Noto Sans Modi** — which (importantly for us) let us *render* Modi images from known Marathi text to create synthetic training data.
- **Keyboard.** A Modi keyboard layout ("Modi KaGaPa Phonetic") ships in the Linux XKB stack.
- **Revival.** A revival movement began in **Pune in 2014**; by 2025 several hundred students had been trained, and some schools have begun teaching Modi again. Renewed public interest (including genealogical and historical research) has added momentum.

---

## 8. Why this matters for our project

Every challenge in Section 4 — no word spaces, cursive ligatures, look-alike letters, and style drift across the Shivakalin, Peshwekalin, and Anglakalin eras — is something our pipeline and our annotation guidelines must explicitly handle. And every fact in Sections 6–7 explains both the **urgency** (readers are vanishing, documents are decaying) and the **opportunity** (Unicode + open fonts make digitization and synthetic data possible). The better the whole team understands the script, the better our dataset and our human review will be.

---

## 9. Sources & further reading (authoritative)

These are the original sources this tutorial draws on. The first two are the most authoritative for, respectively, the script's encoding/structure and its historical decline.

1. **Pandey, Anshuman (2011).** *N4034: Proposal to Encode the Modi Script in ISO/IEC 10646.* ISO/IEC JTC1/SC2/WG2. — The primary technical/scholarly reference for Modi's structure and Unicode encoding. https://www.unicode.org/L2/L2011/11212r2-n4034-modi.pdf
2. **Sohoni, Pushkar (2017).** "Marathi of a Single Type: The Demise of the Modi Script." *Modern Asian Studies* 51(3): 662–685. DOI: 10.1017/S0026749X15000542 — Peer-reviewed account of why Modi declined.
3. **Bhimraoji, Rajendra / Thakre (2014).** "Reviving the Modi Script." *Typography Day (Typoday)* 2014. — Era styles (Chitnisi, Bilavalkari, Mahadevpanti, Ranadi) and calligraphic evolution.
4. **C-DAC.** "Modi-Script Tools." Centre for Development of Advanced Computing (Government of India). https://www.cdac.in — Background on Modi as administrative shorthand and its periodization.
5. **"Towards Modi Script Preservation: Tools for Digitization."** *CS & IT (AIRCC)* conference paper. https://aircconline.com/csit/papers/vol12/csit121305.pdf — Era-by-era calligraphic changes and digitization context.
6. **Wikipedia: "Modi script."** https://en.wikipedia.org/wiki/Modi_script — Useful consolidated overview; cites the primary sources above.
7. **Kausadikar, Kale, Susladkar, Mittal (2025).** *Historic Scripts to Modern Vision* (MoDeTrans/MoScNet). arXiv:2503.13060; ICDAR 2025, Springer LNCS, DOI 10.1007/978-3-032-04630-7_3 — The era split (Shivakalin/Peshwekalin/Anglakalin) used by our reference dataset.
8. **Kulkarni, Borde, Manza, Yannawar (2014).** "Offline Handwritten MODI Character Recognition Using Hu, Zernike Moments and Zoning." arXiv:1406.6140 — Early Modi OCR.

*(Dates and details above were taken from these sources; please verify any specific claim against the original before citing it formally in a publication.)*

---

## Appendix — Era quick-reference for annotators

| If a document is from… | Expect… | Watch for… |
|---|---|---|
| Shivakalin (17th c.) | Chitnisi style, more standardized | Older orthographic conventions |
| Peshwekalin (18th–early 19th c.) | Highly cursive; multiple sub-styles | Style variation *within* the era (Chitnisi/Bilavalkari/Mahadevpanti/Ranadi) |
| Anglakalin (1818–1952) | Nib-pen look, thick–thin strokes | Mixed Modi/English context; later spelling shifts |


