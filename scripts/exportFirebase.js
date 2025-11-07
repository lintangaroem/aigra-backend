import { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs } from "firebase/firestore";
import { createObjectCsvWriter } from "csv-writer";

// Konfigurasi Firebase
const firebaseConfig = {
  apiKey: "AIzaSyBPLcxZWk3__v0dYdyEAYuI1WWppDRBbY4",
  authDomain: "aigraindonesia-3a0f0.firebaseapp.com",
  projectId: "aigraindonesia-3a0f0",
  storageBucket: "aigraindonesia-3a0f0.firebasestorage.app",
  messagingSenderId: "613335127697",
  appId: "1:613335127697:web:f8b9af3bcf43704b861130"
};

// Inisialisasi Firebase dan Firestore
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Fungsi utama untuk ekspor
async function exportToCSV() {
  try {
    const querySnapshot = await getDocs(collection(db, "prototype_silo"));
    
    // Ambil semua dokumen dan ubah jadi array data
    const data = querySnapshot.docs.map(doc => {
      const d = doc.data();
      return {
        id: doc.id,
        suhu: d.suhu ?? "",
        kelembaban: d.kelembaban ?? "",
        mq135: d.mq135 ?? "",
        status: d.status ?? "",
        timestamp: d.timestamp?.toDate ? d.timestamp.toDate().toISOString() : ""
      };
    });

    if (data.length === 0) {
      console.log("⚠️ Tidak ada data di koleksi Firestore.");
      return;
    }

    // Buat writer CSV
    const csvWriter = createObjectCsvWriter({
      path: "data_realtime.csv",
      header: [
        { id: "id", title: "ID" },
        { id: "suhu", title: "Suhu" },
        { id: "kelembaban", title: "Kelembaban" },
        { id: "mq135", title: "CO2 (MQ135)" },
        { id: "status", title: "Status" },
        { id: "timestamp", title: "Timestamp" }
      ]
    });

    // Tulis ke file CSV
    await csvWriter.writeRecords(data);
    console.log(`✅ Berhasil menulis ${data.length} data ke file data_realtime.csv`);

  } catch (error) {
    console.error("❌ Error saat ekspor data:", error);
  }
}

exportToCSV();
