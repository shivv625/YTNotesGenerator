const PDFDocument = require("pdfkit");
const stream = require("stream");

exports.handler = async function (event, context) {
  try {
    if (event.httpMethod !== "POST") {
      return {
        statusCode: 405,
        body: JSON.stringify({ error: "Method Not Allowed" }),
      };
    }

    const { notes, title } = JSON.parse(event.body);
    if (!notes || !title) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Missing notes or title" }),
      };
    }

    // Create PDF in memory
    const doc = new PDFDocument();
    let buffers = [];
    doc.on("data", buffers.push.bind(buffers));
    doc.on("end", () => {});

    // Title
    doc.fontSize(20).text(title, { align: "center", underline: true });
    doc.moveDown();
    // Notes (basic markdown-like formatting)
    notes.split("\n").forEach((line) => {
      if (line.startsWith("# ")) {
        doc.fontSize(16).text(line.replace("# ", ""), { underline: true });
      } else if (line.startsWith("## ")) {
        doc.fontSize(14).text(line.replace("## ", ""), { underline: true });
      } else if (line.startsWith("- ") || line.startsWith("• ")) {
        doc.fontSize(12).text(line, { indent: 20 });
      } else {
        doc.fontSize(12).text(line);
      }
    });
    doc.end();

    // Wait for PDF to finish
    const pdfBuffer = await new Promise((resolve, reject) => {
      const bufs = [];
      doc.on("data", (d) => bufs.push(d));
      doc.on("end", () => resolve(Buffer.concat(bufs)));
      doc.on("error", reject);
    });

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="${title.replace(
          /[^a-z0-9]/gi,
          "_"
        )}.pdf"`,
      },
      body: pdfBuffer.toString("base64"),
      isBase64Encoded: true,
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
