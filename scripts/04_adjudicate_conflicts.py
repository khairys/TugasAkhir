import os
import sys
import re
import json
import logging
import hashlib
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/04_adjudicate_conflicts.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

ADJUDICATIONS_BY_TEXT = {
    # Gambling promotions (canonical_label = "1")
    "Artis4D Member baru pasti jepe": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Promotional claim and endorsement of gambling site 'Artis4D' with claim 'pasti jepe'. Misannotated as 0 in DS4.",
        "note": "Section 6E (Brand/site endorsement) & 6C (Promotional claim)."
    },
    "Gasskuyy dari bang toing katanya,Ga ruda-Ho ki-Badai petir🔥🔥": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Obfuscated gambling promotion with separated syllables 'Ga ruda-Ho ki' (Garuda Hoki) and slot reference 'Badai petir' (Zeus slot).",
        "note": "Section 6F (Obfuscated promotion)."
    },
    "Sumpah.Garuda Ho ki-beneran gampang banget jepe nya, bukan sekadar iklan sampah👊": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Testimonial and social proof endorsement for site 'Garuda Hoki' with claim 'gampang jepe'. Misannotated as 0 in DS4.",
        "note": "Section 6D (Testimonial/social proof)."
    },
    "0:56 WiFi4D bukti nyata, bukan sekadar janji.🎉": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Promotional spam with fake YouTube timestamp and brand endorsement for 'WiFi4D'. Misannotated as 0 in DS4.",
        "note": "Section 6E (Brand endorsement) & 6F (Timestamp obfuscation)."
    },
    "Aku pertama depo jp diGaruda-Ho ki😚": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Testimonial and endorsement promoting deposit and winning at Garuda Hoki. Misannotated as 0 in 1 row of DS4.",
        "note": "Section 6D (Testimonial/social proof)."
    },
    "Keberuntungan saya bener-bener gacir di T O K E 6 9 nggak nyangka!": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Obfuscated endorsement with spaced characters 'T O K E 6 9' (Toke69) and promotional claim 'gacir'.",
        "note": "Section 6D & 6F."
    },
    "Kalau seperti itu pasti ga bakalan kalah dong 🍭𝑺𝑬𝑵𝑫𝑨𝑳4𝑫🍭": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Promotional endorsement for gambling site 'SENDAL4D' using mathematical italic unicode font. Misannotated as 0 in DS4.",
        "note": "Section 6E & 6F."
    },
    "kalau mukbang paling enak sambil buka 𝐓𝐀𝐊𝐉𝐔𝐁𝟒𝐃 sudah pasti di kasih jajan sampai puas!!!": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Promotional CTA for gambling platform 'TAKJUB4D' with promise of bonus ('kasih jajan sampai puas'). Misannotated as 0 in DS4.",
        "note": "Section 6A & 6F."
    },
    "Ga Ruda Ho ki-gokil banget pecah terus ga sia sia anjaay🔥": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Obfuscated endorsement for Garuda Hoki with claim of continuous win ('pecah terus'). Misannotated as 0 in 1 row of DS4.",
        "note": "Section 6D & 6F."
    },
    "wadaw BERKAH99": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Brand mention/shoutout for gambling site 'BERKAH99'. Misannotated as 0 in DS4.",
        "note": "Section 6E."
    },
    "apalagi ini 07:01 Ｐ ＵＬ Ａ Ｕ W I N ⚡️": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Obfuscated brand endorsement for 'PULAUWIN' using full-width characters and timestamp. Internal duplicate conflict in DS2 resolved to 1.",
        "note": "Section 6E & 6F."
    },
    "Sangat keren! Meraih kemenangan besar di ambil4d langsung berlibur ke luar negeri!": {
        "canonical_label": "1",
        "decision": "ACCEPT_PROMOTION",
        "reason": "Fabricated bot testimonial promoting site 'ambil4d'. Internal duplicate conflict in DS5 resolved to 1.",
        "note": "Section 6D."
    },

    # Ambiguous / uncertain cases (canonical_label = None, review queue)
    "Seriusan bang ? Gua zonk terus nih main di situs lain 😢😂": {
        "canonical_label": None,
        "decision": "SEND_TO_REVIEW",
        "reason": "Ambiguous interaction: could be bot baiting for a site link or a genuine user expressing frustration in a spam thread. Sent to review queue.",
        "note": "Section 10 (Uncertain label)."
    },
    "Ajak family lu aja main,kali aja JP 😂": {
        "canonical_label": None,
        "decision": "SEND_TO_REVIEW",
        "reason": "Ambiguous teasing comment mentioning 'JP'. Could be sarcasm between gaming friends or gambling banter. Sent to review queue.",
        "note": "Section 10."
    },
    "Pake server Kamboja ketua biar menang terus": {
        "canonical_label": None,
        "decision": "SEND_TO_REVIEW",
        "reason": "Ambiguous advice referencing 'server Kamboja'. Could be streaming joke teasing or actual gambling tip. Sent to review queue.",
        "note": "Section 10."
    },

    # Non-promotions (canonical_label = "0")
    "Situs sampah , jp kagak Rungkat iya wkwkwk": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Criticism and expression of player frustration ('situs sampah, rungkat'). Does not promote gambling. Misannotated as 1 in DS4.",
        "note": "Section 7B (Kritik/diskusi) & 7C (Keluhan)."
    },
    "Tul,bener\" menghibur banget beliau beliau ini,apalagi max,": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "General entertainment comment on a YouTube gaming/streaming video. No gambling relation. Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar biasa YouTube)."
    },
    "gemes banget liat ini orang main miya kyk gapunya skill 1, pencet lah pencett itu nggak cuma nyebar damage ada bonusnyaa juga meski musuh sendirian abangggg": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Mobile Legends gaming gameplay discussion regarding hero Miya. Misannotated as 1 in DS4 due to keyword 'bonus'.",
        "note": "Section 7E (Konteks non-judi) & Section 8 (Jangan keyword-only)."
    },
    "3:12 Rinz berpikir dia assassin tank... jalan polos banget kek player epic baru maen... 😂😂": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Mobile Legends esports/gameplay commentary about player Rinz. Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar biasa YouTube gaming)."
    },
    "😂😂😂si kecil aktif gitu co bisa aja pascol ngundang orang\"": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Viewer reaction to streamer Pascol video content. Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar umum)."
    },
    "Dari semua mantan player tevos si max paling besar mulut exp masa depan lawan rrq udah telor gmna lawan raja terakhir onic": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Esports banter regarding Mobile Legends team EVOS, RRQ, and ONIC. Misannotated as 1 in DS4.",
        "note": "Section 7F (Diskusi esports non-judi)."
    },
    "Hama puki": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Profanity/toxic banter from gaming audience. Contains no gambling promotion. Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar umum non-judi)."
    },
    "\"Raja dari segala raja\"😂😂😂": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Teasing the nickname of RRQ Mobile Legends team ('Raja dari segala raja'). Misannotated as 1 in DS4.",
        "note": "Section 7F (Diskusi esport)."
    },
    "Gua dulu pernah fans RRQ jaman TUTURU.... setelah itu gua fans ONIC sampai sekarang ......... Tau sendiri kan RRQ skrg cuma bacot sama teori saja yg gede, fakta dan praktek nya nihil alias HAMPA.... 😂😂😂😂😂,  Gini kok di bilang raja dari segala raja ... Hahaha MEMEEEKKKK MEMEEEKKKK": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Long fan commentary on RRQ Tuturu vs ONIC esports. Misannotated as 1 in DS4.",
        "note": "Section 7F (Diskusi esport)."
    },
    "Bang bikent vibes nya udah beda banget udah ga berapi api kaya dulu 😔": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Comment directed to YouTuber Brandon Kent (Bikent). Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar streamer)."
    },
    "Bener² udah gak niat ngonten😂 thumbnailnya udah 2jam blm di ganti² yang match 1🤣": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Comment criticizing channel uploader for slow thumbnail update on match 1. Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar YouTube)."
    },
    "menang di puja\"kalah di taik\"in.gimna sih.": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "General moral sentiment about audience hypocrisy in sports/games. Misannotated as 1 in DS4.",
        "note": "Section 7F (Komentar umum)."
    },
    "Rrq bukan cari juara, tapi cuma cari cuan": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Criticism of RRQ esports organization commercial focus. Misannotated as 1 in DS4 due to keyword 'cuan'.",
        "note": "Section 7F & Section 8."
    },
    "Selalu menghibur ketua naga hitam yang satu ini": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Fan comment appreciating video creator/streamer. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "gua jg bingung, gua memang dukung RRQ tapi di Onic ada skylar dan di Evos ada albert vyn😂 jadi harus 3 nih": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Esports discussion about pro players Skylar, Albert, and Vyn. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "min, tumben skrng upload video keratua kok gak pake efek editan": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Audience question to YouTube channel admin regarding video editing effects. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Liat notifnya aj udh ngakak": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Reaction to YouTube video notification. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Niatnya beli lc buat dibully ini malah labi labi yg kena buly🤣": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Gaming stream joke. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Hayo mana fans Yamal katanya Yamal daptkan balon dor tapi apa 🤫😁🗿😅": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Football discussion about Lamine Yamal and Ballon d'Or. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Memang palua ⚡  Vyn Uciha gak mainin rendy aneh banget, sibuk doang gonta ganti pemain, pemai": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Esports critique regarding MLBB pro player Vyn. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Jangan di paksa maju di keroyok juga kalah": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Advice on in-game team fight tactical movement. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Tutor Garuda bang 🗿🤌🤌": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Viewer asking for tutorial on game hero/mechanic. Not a gambling promo. Misannotated as 1 in DS4.",
        "note": "Section 7E & 7F."
    },
    "Lucu banget 😂😂😂": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Standard humorous reaction to YouTube video. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Review hero baru yg tolol cuma pascol": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Critique of streamer Pascol reviewing a new ML hero. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Sejak lu sukses besar gak ada lagi kuliat kau ngajak kak Luan Mabar ya col": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Personal remark to streamer Pascol about playing games with LuanLuan. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Luan2 apa kabar ketua": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Asking about streamer LuanLuan. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Padahal udah pada tau kunci onic itu di duo mid sama roam dan kebiasaan rrq gonta ganti pemain di mpl 😅 kocak banget gimana mau kemestri": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Esports tactical analysis of ONIC vs RRQ in MPL. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Max win apa maxim": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Wordplay pun between gambling term 'maxwin' and ride-hailing app 'Maxim'. Not promoting gambling. Misannotated as 1 in DS4.",
        "note": "Section 7D & 7F."
    },
    "Apalah marah mulu, udah gitu nafsu": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Reaction to streamer gaming rage behavior. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "RRQ sudah menjadi bisnis seperti Evos jaman dulu": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Commentary on commercialization of esports organizations. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Bonus ketua": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Streamer gaming community inside joke. Misannotated as 1 in DS4 due to keyword 'bonus'.",
        "note": "Section 7E & Section 8."
    },
    "Terpercaya dan proses paling cepat memang di ourastoree": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Endorsement for authorized Mobile Legends game top-up diamond store ('ourastoree' owned by streamer Oura Eko), not online gambling. Misannotated as 1 in DS4.",
        "note": "Section 7E (Konteks non-judi)."
    },
    "Jadi apa masalahnya setiap orang ada urusan masing-masing": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "General audience comment about personal boundaries. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Wkwk awal season udah push aj lu col": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Chat remark to streamer Pascol about early season rank pushing in Mobile Legends. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Evos bak to kandang kucing": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Esports banter mocking team EVOS. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    },
    "Ketua aku bangun tidur dituduh selingkuh tanpa ada leher😂😂😂": {
        "canonical_label": "0",
        "decision": "ACCEPT_NON_PROMOTION",
        "reason": "Humorous viewer comment in livestream. Misannotated as 1 in DS4.",
        "note": "Section 7F."
    }
}

def main():
    logging.info("Memulai Phase 4: Label Conflict Adjudication by Text")
    df = pd.read_pickle("data/interim/full_pool_hashed.pkl")
    
    conflict_mask = df["is_label_conflict"] == True
    logging.info(f"Total conflict records flagged in pool: {conflict_mask.sum()}")
    
    conflict_audit_rows = []
    updated_records = 0
    
    # Process each conflict record
    for idx, row in df[conflict_mask].iterrows():
        txt = str(row["text_raw"])
        adj = ADJUDICATIONS_BY_TEXT.get(txt)
        if not adj:
            # Try stripped
            adj = ADJUDICATIONS_BY_TEXT.get(txt.strip())
            
        if adj:
            c_lbl = adj["canonical_label"]
            decision = adj["decision"]
            reason = adj["reason"]
            note = adj["note"]
            
            lbl_status = "accepted" if c_lbl is not None else "review"
            
            df.at[idx, "canonical_label"] = c_lbl
            df.at[idx, "label_status"] = lbl_status
            df.at[idx, "label_reason"] = f"conflict_adjudication: {decision}"
            df.at[idx, "adjudication_note"] = f"{reason} | {note}"
            updated_records += 1
            
            conflict_audit_rows.append({
                "record_id": row["record_id"],
                "exact_hash": row["exact_hash"],
                "text_raw": txt,
                "source_dataset": row["source_dataset"],
                "source_row_id": row["source_row_id"],
                "source_label": row["source_label"],
                "canonical_label": c_lbl if c_lbl is not None else "NULL",
                "label_status": lbl_status,
                "decision": decision,
                "reason": reason,
                "adjudication_note": note
            })
        else:
            logging.warning(f"Unmatched conflict text: {txt[:50]}")
            
    logging.info(f"Successfully adjudicated and updated: {updated_records} / {conflict_mask.sum()} conflict records.")
    
    # Save label_conflicts.csv
    conflict_df = pd.DataFrame(conflict_audit_rows)
    conflict_df.to_csv("data/audit/label_conflicts.csv", index=False, encoding="utf-8")
    logging.info(f"Saved data/audit/label_conflicts.csv ({len(conflict_df)} rows).")
    
    # Save updated full pool
    df.to_pickle("data/interim/full_pool_adjudicated.pkl")
    df.to_csv("data/interim/full_pool_adjudicated.csv", index=False, encoding="utf-8")
    logging.info("Saved data/interim/full_pool_adjudicated.pkl and .csv")

if __name__ == "__main__":
    main()
