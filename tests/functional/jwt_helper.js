import KJUR from "jsrsasign";
import { v4 as uuidv4 } from "uuid";
import JSONWebKey from "json-web-key";
import jose from "node-jose";
import crypto from "crypto";

const JWK = jose.JWK;
const JWE = jose.JWE;

const signingKeyString =
  "-----BEGIN RSA PRIVATE KEY-----\n" +
  "MIIEogIBAAKCAQEAvZzMraB96Wd1zfHS3vW3z//Nkqz+9HfwViNje2Y5L6m3K/7r\n" +
  "aA0kUsWD1f6X7/LIJfkCEctCEj9q19+cX30h0pi6IOu92MlIwdH/L6CTuzYnG4PA\n" +
  "CKT8FZonLw0NYBqh8p4vWS8xtNHNjTWua/FFTlxdtYnEb9HbUZkg7dXAtnikozlE\n" +
  "/ZZSponq7K00h3Uh9goxQIavcK1QI8pw5V+T8V8Ue7k98W8LpbYQWm7FPOZayu1E\n" +
  "oJWUZefdOlYAdeVbDS4tjrVF+3za+VX3q73zJEfyLEM0zKrkQQ796gfYpkzDYwJv\n" +
  "kiW7fb2Yh1teNHpFR5tozzMwUxkREl/TQ4U1kwIDAQABAoIBAHXiS1pTIpT/Dr24\n" +
  "b/rQV7RIfF2JkoUZIGHdZJcuqbUZVdlThrXNHd0cEWf0/i9fCNKa6o93iB9iMCIA\n" +
  "Uu8HFAUjkOyww/pIwiRGU9ofglltRIkVs0lskZE4os3c1oj+Zds6P4O6FLQvkBUP\n" +
  "394aRZV/VX9tJKTEmw8zHcbgEw0eBpiY/EMELcSmZYk7lhB80Y+idTrZcHoV4AZo\n" +
  "DhQwyF0R63mMphuOV4PwaCdCYZKgd/tr2uUHglLpYbQag3iEzoDfxdFcxnRkBdOi\n" +
  "a/wcNo0JRlMsxXmtJ+HrZar+6ObUx5SgLGz7dQnKvP/ZgenTk0yyohwikh2b2KOS\n" +
  "M3M2oUkCgYEA9+olFPDZxtM1fwmlXcymBtokbiki/BJQGJ1/5RMqvdsSeq8icl/i\n" +
  "Qk5AoNbWEcsAxeBftb1IfnxJsRthRyp0NX5HOSsBFiIfdSF225nmBpktwPjJmvZZ\n" +
  "G2MQCVqw9Y40Cia0LZnRo8417ahSfVf8/IoggnAwkswJ3fkktt/FlW8CgYEAw8vi\n" +
  "7hWxehiUaZO4RO7GuV47q4wPZ/nQvcimyjJuXBkC/gQay+TcA7CdXQTgxI2scMIk\n" +
  "UPas36mle1vbAp+GfWcNxDxhmSnQvUke4/wHF6sNZ3BwKoTRqJqFcFUHm+2uo6A4\n" +
  "HCBtXM83Z1nDYkHUrfng99U+zgGDz2XKPko9OB0CgYAtVVOSkLhB8z1FDa5/iHyT\n" +
  "pDAlNMCA95hN5/8LFIYsUXL/nCbgY0gsd8K5po9ekZCCnpTh1sr61h9jk24mZUz6\n" +
  "uyyq94IrWfIGqSfi4DF/42LKdrPm8kU5DNRR4ZOaU3aQpKMt84KyQXL7ElyDLyPD\n" +
  "yj5Hm9xF+6mSPYzJJAItYQKBgHzUZXbzf7ZfK2fwVSAlt68BJDvnzP62Z95Hqgbp\n" +
  "hjDThXPbvBXYcGkt1fYzIPZPeOxe6nZv/qGOcEGou4X9nOogpMdC09qprTqw/q/N\n" +
  "w9vUI3SaW/jPuzeqZH7Mx1Ajhh8uC/fquK7eMe2Dbi0b2XOeB08atrLyhk3ZEMsL\n" +
  "2+IFAoGAUbmo0idyszcarBPPsiEFQY2y1yzHMajs8OkjUzOVLzdiMkr36LF4ojgw\n" +
  "UCM9sT0g1i+eTfTcuOEr3dAxcXld8Ffs6INSIplvRMWH1m7wgXMRpPCy74OuxlDQ\n" +
  "xwPp/1IVvrMqVgnyS9ezAeE0p9u8zUdZdwHz1UAggwbtHR6IbIA=\n" +
  "-----END RSA PRIVATE KEY-----\n";

const encryptionKeyString =
  "-----BEGIN PUBLIC KEY-----\n" +
  "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt8LZnIhuOdL/BC029GOa\n" +
  "JkVUAqgp2PcmbFr2Qwhf/514DUUQ9sKJ1rvwvbmmW2zE8JRtdY3ey0RXGtMn5UZH\n" +
  "s8NReHzMxvsmHN4VuaGEnFmPwO821Tkvg0LpKsLkotcw793FD/fut44N2lhpTSW2\n" +
  "Sc82uG0p9A+Kud8HCIaWaluosghk9rbMGYDzZQk8cA91GtKJRmIOED4PorB/dexD\n" +
  "f37qhuWNQgzyNyTti1DTDUIWyzQQJp926vLbkOip6Fc2R13hOFNETe68Rrw/h3hX\n" +
  "EFS17uPFZHsxvm9PFXX9KZMS25ohqbNh97I94LL4o4wybl6LaE6lJEHiD6docD0B\n" +
  "6wIDAQAB\n" +
  "-----END PUBLIC KEY-----\n";

const schemaRegEx = /^([a-z0-9]+)_(\w+)\.json/;

export function getRandomString(length) {
  let result = "";
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

export function generateToken(
  schema,
  {
    version,
    theme,
    userId,
    collectionId,
    responseId,
    surveyId = "123",
    periodId = "201605",
    periodStr = "May 2016",
    ruRef = "12346789012A",
    sdsDatasetId = null,
    regionCode = "GB-ENG",
    languageCode = "en",
    includeLogoutUrl = true,
    displayAddress = "",
  }
) {
  const schemaParts = schemaRegEx.exec(schema);

  // Header
  const oHeader = {
    alg: "RS256",
    typ: "JWT",
    kid: "709eb42cfee5570058ce0711f730bfbb7d4c8ade",
  };

  // Payload
  let payload = {};
  const txId = uuidv4();
  const jti = uuidv4();
  const iat = KJUR.jws.IntDate.get("now");
  const exp = KJUR.jws.IntDate.get("now") + 1800;
  const caseId = uuidv4();
  const currentDate = new Date();
  currentDate.setUTCDate(currentDate.getUTCDate() + 1);
  const isoDate = currentDate.toISOString();

  if (version === "v2") {
    payload = {
      tx_id: txId,
      jti: jti,
      iat: iat,
      exp: exp,
      case_id: caseId,
      response_id: responseId,
      schema_name: `${schemaParts[1]}_${schemaParts[2]}`,
      collection_exercise_sid: collectionId,
      region_code: regionCode,
      language_code: languageCode,
      account_service_url: "http://localhost:8000",
      survey_metadata: getSurveyMetadata(theme, userId, displayAddress, surveyId, periodId, periodStr, ruRef, sdsDatasetId),
      version: "v2",
      response_expires_at: isoDate,
    };
  } else {
    payload = {
      tx_id: txId,
      jti: jti,
      iat: iat,
      exp: exp,
      user_id: userId,
      case_id: caseId,
      ru_ref: "12346789012A",
      response_id: responseId,
      ru_name: "Apple",
      trad_as: "Apple",
      schema_name: `${schemaParts[1]}_${schemaParts[2]}`,
      collection_exercise_sid: collectionId,
      period_id: periodId,
      period_str: periodStr,
      ref_p_start_date: "2017-01-01",
      ref_p_end_date: "2017-02-01",
      employment_date: "2016-06-10",
      return_by: "2017-03-01",
      display_address: displayAddress,
      region_code: regionCode,
      language_code: languageCode,
      account_service_url: "http://localhost:8000",
      response_expires_at: isoDate,
    };
  }

  const oPayload = payload;

  if (includeLogoutUrl) {
    oPayload.account_service_log_out_url = "http://localhost:8000";
  }

  // Sign JWT, password=616161
  const sHeader = JSON.stringify(oHeader);
  const sPayload = JSON.stringify(oPayload);

  const prvKey = KJUR.KEYUTIL.getKey(signingKeyString, "digitaleq");

  const sJWT = KJUR.jws.JWS.sign("RS256", sHeader, sPayload, prvKey);

  const webKey = JSONWebKey.fromPEM(encryptionKeyString);

  const shasum = crypto.createHash("sha1");
  shasum.update(encryptionKeyString);
  const encryptionKeyKid = shasum.digest("hex");

  return JWK.asKey(webKey.toJSON())
    .then((jwk) => {
      const cfg = {
        contentAlg: "A256GCM",
      };
      const recipient = {
        key: jwk,
        header: {
          alg: "RSA-OAEP",
          kid: encryptionKeyKid,
        },
      };
      const jwe = JWE.createEncrypt(cfg, recipient);
      return jwe.update(sJWT).final();
    })
    .then((result) => {
      const token = `${result.protected}.${result.recipients[0].encrypted_key}.${result.iv}.${result.ciphertext}.${result.tag}`;

      return token;
    });
}

function getSurveyMetadata(theme, userId, displayAddress, surveyId, periodId, periodStr, ruRef, sdsDatasetId) {
  let surveyMetadata = {};

  if (theme === "social") {
    surveyMetadata = {
      data: {
        case_ref: "1000000000000001",
        qid: "1000000000000001",
      },
      receipting_keys: ["qid"],
    };
  } else {
    surveyMetadata = {
      data: {
        user_id: userId,
        display_address: displayAddress,
        ru_ref: ruRef,
        survey_id: surveyId,
        period_id: periodId,
        period_str: periodStr,
        sds_dataset_id: sdsDatasetId,
        ref_p_start_date: "2017-01-01",
        ref_p_end_date: "2017-02-01",
        employment_date: "2016-06-10",
        return_by: "2017-03-01",
        ru_name: "Apple",
        trad_as: "Apple",
      },
    };
  }

  return surveyMetadata;
}
