from flask import Flask, request, jsonify
from openai import OpenAI
client = OpenAI(
    api_key="sk-proj-8K8nhobsMSYPb4UQgSkGT3BlbkFJJFM8GLyG4xcH7BwoG6la",
)

app = Flask(__name__)

@app.route("/recommendation", methods=["POST"])
def recommendation():
    if request.is_json:
        data = request.get_json()
        print(data)
        startingPoint = data.get("startingPoint")
        destination = data.get("destination")
        budget = data.get("budget")
        stay = data.get("stay")
        peopleCount = data.get("peopleCount")

        if (startingPoint is None or startingPoint == "") or (destination is None or destination == "") or (budget is None or budget == "") or (stay is None or stay == "") or (peopleCount is None or peopleCount == ""):
            return jsonify({"status": False, "content": "Missing required parameters"}), 400
        else:
            try:
                prompt = f"saya mempunyai budget sekitar {budget} untuk liburan ke {destination} dari {destination}, total {peopleCount} orang , dengan durasi liburan {stay} hari, buat rincian wisata(beserta transportasi ke wisatanya), hotel (spesifik nama hotel nya, cari hotel yang dekat dengan semua wisata), dll saat liburan dengan lengkap; perintah penting: jawab dengan format html yang diberi sedikit styling css agar lebih rapih untuk dapat ditampilkan didalam aplikasi iOS (Swift). Jadi jawab saja langsung dengan kode html tanpa di tambahkan text apapun. isi html buat sedikit rapi dengan membagi menjadi beberapa section yang berbeda."
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                            {"role": "system", "content": "Anda adalah asisten perjalanan yang terampil dalam memberikan rekomendasi tempat wisata berdasarkan budget, jumlah orang, dan total hari."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                return jsonify({"status": True, "content": response.choices[0].message.content.replace('```html\n', '').replace('```', '')}), 200
            except Exception as e:
                return jsonify({"status": False, "content": str(e)}), 500
    else:
        return jsonify({"status": False, "content": "Request is not JSON"}), 400        