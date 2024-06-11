const express = require("express");
const app = express();
const port = process.env.Port || 3000;
const Cloudant = require("@cloudant/cloudant");
const IAM_API_KEY = process.env.IAM_API_KEY;
const CLOUDANT_URL = process.env. CLOUDANT_URL;

//Initilaizecloudant connection with IAM authentication
// Get API key and CLOUDANT URL from Cloudant Account
// Use config or .env to set CLOUDANT URL & APIKEY

async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: IAM_API_KEY} },
            url: CLOUDANT_URL,
        });

    const db = cloudant.use("dealerships");
    console.info("Connection success! Connected to DB");
    return db;
    } catch (err) {
        console.error("Connect failure: " + err.message + " for Cloudant DB");
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

app.get("/dealership/get", (req, res) => {
    const { state, id } = req.query;

    // Create a selector object based on query parameters 
    const selector = {};
    if (state) {
        selector.state = state;
    }

    if(id) {
        selector.id = parseInt(id); //Filter by "id" 
    }

    const queryOptions = {
        selector,
        limit: 10,
    }

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error("Error fetching dealership:", err);
            res
              .status(500)
              .json({ error: "An error occurred while fetching dealerships." });
        } else {
          const dealerships = body.docs;
          res.json(dealerships);
        }
    });
})

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });