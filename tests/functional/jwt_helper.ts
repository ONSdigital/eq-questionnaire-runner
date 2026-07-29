import KJUR from 'jsrsasign'
import { v4 as uuidv4 } from 'uuid'
import JSONWebKey from 'json-web-key'
import jose from 'node-jose'
import crypto from 'crypto'

const JWK = jose.JWK
const JWE = jose.JWE

const signingKeyString =
  '-----BEGIN RSA PRIVATE KEY-----\n' +
  'MIIEogIBAAKCAQEAvZzMraB96Wd1zfHS3vW3z//Nkqz+9HfwViNje2Y5L6m3K/7r\n' +
  'aA0kUsWD1f6X7/LIJfkCEctCEj9q19+cX30h0pi6IOu92MlIwdH/L6CTuzYnG4PA\n' +
  'CKT8FZonLw0NYBqh8p4vWS8xtNHNjTWua/FFTlxdtYnEb9HbUZkg7dXAtnikozlE\n' +
  '/ZZSponq7K00h3Uh9goxQIavcK1QI8pw5V+T8V8Ue7k98W8LpbYQWm7FPOZayu1E\n' +
  'oJWUZefdOlYAdeVbDS4tjrVF+3za+VX3q73zJEfyLEM0zKrkQQ796gfYpkzDYwJv\n' +
  'kiW7fb2Yh1teNHpFR5tozzMwUxkREl/TQ4U1kwIDAQABAoIBAHXiS1pTIpT/Dr24\n' +
  'b/rQV7RIfF2JkoUZIGHdZJcuqbUZVdlThrXNHd0cEWf0/i9fCNKa6o93iB9iMCIA\n' +
  'Uu8HFAUjkOyww/pIwiRGU9ofglltRIkVs0lskZE4os3c1oj+Zds6P4O6FLQvkBUP\n' +
  '394aRZV/VX9tJKTEmw8zHcbgEw0eBpiY/EMELcSmZYk7lhB80Y+idTrZcHoV4AZo\n' +
  'DhQwyF0R63mMphuOV4PwaCdCYZKgd/tr2uUHglLpYbQag3iEzoDfxdFcxnRkBdOi\n' +
  'a/wcNo0JRlMsxXmtJ+HrZar+6ObUx5SgLGz7dQnKvP/ZgenTk0yyohwikh2b2KOS\n' +
  'M3M2oUkCgYEA9+olFPDZxtM1fwmlXcymBtokbiki/BJQGJ1/5RMqvdsSeq8icl/i\n' +
  'Qk5AoNbWEcsAxeBftb1IfnxJsRthRyp0NX5HOSsBFiIfdSF225nmBpktwPjJmvZZ\n' +
  'G2MQCVqw9Y40Cia0LZnRo8417ahSfVf8/IoggnAwkswJ3fkktt/FlW8CgYEAw8vi\n' +
  '7hWxehiUaZO4RO7GuV47q4wPZ/nQvcimyjJuXBkC/gQay+TcA7CdXQTgxI2scMIk\n' +
  'UPas36mle1vbAp+GfWcNxDxhmSnQvUke4/wHF6sNZ3BwKoTRqJqFcFUHm+2uo6A4\n' +
  'HCBtXM83Z1nDYkHUrfng99U+zgGDz2XKPko9OB0CgYAtVVOSkLhB8z1FDa5/iHyT\n' +
  'pDAlNMCA95hN5/8LFIYsUXL/nCbgY0gsd8K5po9ekZCCnpTh1sr61h9jk24mZUz6\n' +
  'uyyq94IrWfIGqSfi4DF/42LKdrPm8kU5DNRR4ZOaU3aQpKMt84KyQXL7ElyDLyPD\n' +
  'yj5Hm9xF+6mSPYzJJAItYQKBgHzUZXbzf7ZfK2fwVSAlt68BJDvnzP62Z95Hqgbp\n' +
  'hjDThXPbvBXYcGkt1fYzIPZPeOxe6nZv/qGOcEGou4X9nOogpMdC09qprTqw/q/N\n' +
  'w9vUI3SaW/jPuzeqZH7Mx1Ajhh8uC/fquK7eMe2Dbi0b2XOeB08atrLyhk3ZEMsL\n' +
  '2+IFAoGAUbmo0idyszcarBPPsiEFQY2y1yzHMajs8OkjUzOVLzdiMkr36LF4ojgw\n' +
  'UCM9sT0g1i+eTfTcuOEr3dAxcXld8Ffs6INSIplvRMWH1m7wgXMRpPCy74OuxlDQ\n' +
  'xwPp/1IVvrMqVgnyS9ezAeE0p9u8zUdZdwHz1UAggwbtHR6IbIA=\n' +
  '-----END RSA PRIVATE KEY-----\n'

const encryptionKeyString =
  '-----BEGIN PUBLIC KEY-----\n' +
  'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt8LZnIhuOdL/BC029GOa\n' +
  'JkVUAqgp2PcmbFr2Qwhf/514DUUQ9sKJ1rvwvbmmW2zE8JRtdY3ey0RXGtMn5UZH\n' +
  's8NReHzMxvsmHN4VuaGEnFmPwO821Tkvg0LpKsLkotcw793FD/fut44N2lhpTSW2\n' +
  'Sc82uG0p9A+Kud8HCIaWaluosghk9rbMGYDzZQk8cA91GtKJRmIOED4PorB/dexD\n' +
  'f37qhuWNQgzyNyTti1DTDUIWyzQQJp926vLbkOip6Fc2R13hOFNETe68Rrw/h3hX\n' +
  'EFS17uPFZHsxvm9PFXX9KZMS25ohqbNh97I94LL4o4wybl6LaE6lJEHiD6docD0B\n' +
  '6wIDAQAB\n' +
  '-----END PUBLIC KEY-----\n'

const schemaRegEx = /^([a-z0-9]+)_(\w+)\.json/

interface SurveyMetadata {
  data: Record<string, unknown>
  receipting_keys?: string[]
}

interface KjurApi {
  jws: {
    IntDate: {
      get: (value: string) => number
    }
    JWS: {
      sign: (alg: string, header: string, payload: string, privateKey: unknown) => string
    }
  }
  KEYUTIL: {
    getKey: (key: string, passphrase?: string) => unknown
  }
}

interface JsonWebKeyApi {
  fromPEM: (pem: string) => {
    toJSON: () => Record<string, unknown>
  }
}

interface JoseJwkApi {
  asKey: (jwk: Record<string, unknown>) => Promise<unknown>
}

interface JoseJweApi {
  createEncrypt: (
    cfg: { contentAlg: string },
    recipient: JweRecipientInput,
  ) => {
    update: (input: string) => {
      final: () => Promise<JweGeneralSerialization>
    }
  }
}

interface JweRecipientInput {
  key: unknown
  header: {
    alg: string
    kid: string
  }
}

interface JweGeneralSerialization {
  protected: string
  recipients: Array<{
    encrypted_key: string
  }>
  iv: string
  ciphertext: string
  tag: string
}

export interface GenerateTokenOptions {
  launchVersion?: string
  theme?: string
  userId?: string
  collectionId?: string
  responseId?: string
  surveyId?: string
  periodId?: string
  periodStr?: string
  ruRef?: string
  sdsDatasetId?: string | null
  regionCode?: string
  languageCode?: string
  includeLogoutUrl?: boolean
  displayAddress?: string
  booleanFlag?: boolean
}

export function getRandomString (length: number): string {
  let result = ''
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  for (let i = 0; i < length; i += 1) {
    result += characters.charAt(Math.floor(Math.random() * characters.length))
  }
  return result
}

export async function generateToken (
  schema: string,
  {
    launchVersion,
    theme,
    userId,
    collectionId,
    responseId,
    surveyId = '123',
    periodId = '201605',
    periodStr = 'May 2016',
    ruRef = '12345678901A',
    sdsDatasetId = null,
    regionCode = 'GB-ENG',
    languageCode = 'en',
    includeLogoutUrl = true,
    displayAddress = '',
    booleanFlag = false
  }: GenerateTokenOptions
): Promise<string> {
  let schemaParams: Record<string, string> = {}
  if (schema !== '') {
    const schemaParts = schemaRegEx.exec(schema)
    if (schemaParts != null) {
      schemaParams = { schema_name: `${schemaParts[1]}_${schemaParts[2]}` }
    }
  }

  const oHeader = {
    alg: 'RS256',
    typ: 'JWT',
    kid: '709eb42cfee5570058ce0711f730bfbb7d4c8ade'
  }

  const txId = uuidv4()
  const jti = uuidv4()
  const kjur = KJUR as unknown as KjurApi
  const iat = kjur.jws.IntDate.get('now')
  const exp = kjur.jws.IntDate.get('now') + 1800
  const caseId = uuidv4()
  const currentDate = new Date()
  currentDate.setUTCDate(currentDate.getUTCDate() + 1)
  const isoDate = currentDate.toISOString()

  const oPayload: Record<string, unknown> = {
    tx_id: txId,
    jti,
    iat,
    exp,
    case_id: caseId,
    response_id: responseId,
    ...schemaParams,
    collection_exercise_sid: collectionId,
    region_code: regionCode,
    language_code: languageCode,
    account_service_url: 'http://localhost:8000',
    survey_metadata: getSurveyMetadata(theme, userId, displayAddress, surveyId, periodId, periodStr, ruRef, sdsDatasetId, booleanFlag),
    version: launchVersion,
    response_expires_at: isoDate
  }

  if (includeLogoutUrl) {
    oPayload.account_service_log_out_url = 'http://localhost:8000'
  }

  const sHeader = JSON.stringify(oHeader)
  const sPayload = JSON.stringify(oPayload)
  const prvKey = kjur.KEYUTIL.getKey(signingKeyString, 'digitaleq')
  const sJWT = kjur.jws.JWS.sign('RS256', sHeader, sPayload, prvKey)

  const jsonWebKey = JSONWebKey as unknown as JsonWebKeyApi
  const webKey = jsonWebKey.fromPEM(encryptionKeyString)
  const shasum = crypto.createHash('sha1')
  shasum.update(encryptionKeyString)
  const encryptionKeyKid = shasum.digest('hex')

  const jwkApi = JWK as unknown as JoseJwkApi
  const jwk = await jwkApi.asKey(webKey.toJSON())
  const cfg = {
    contentAlg: 'A256GCM'
  }
  const recipient: JweRecipientInput = {
    key: jwk,
    header: {
      alg: 'RSA-OAEP',
      kid: encryptionKeyKid
    }
  }

  const jweApi = JWE as unknown as JoseJweApi
  const result = await jweApi.createEncrypt(cfg, recipient).update(sJWT).final()
  return `${result.protected}.${result.recipients[0].encrypted_key}.${result.iv}.${result.ciphertext}.${result.tag}`
}

function getSurveyMetadata (
  theme: string | undefined,
  userId: string | undefined,
  displayAddress: string,
  surveyId: string,
  periodId: string,
  periodStr: string,
  ruRef: string,
  sdsDatasetId: string | null,
  booleanFlag: boolean
): SurveyMetadata {
  if (theme === 'social') {
    return {
      data: {
        case_ref: '1000000000000001',
        qid: '1000000000000001'
      },
      receipting_keys: ['qid']
    }
  }

  return {
    data: {
      user_id: userId,
      display_address: displayAddress,
      ru_ref: ruRef,
      survey_id: surveyId,
      period_id: periodId,
      period_str: periodStr,
      sds_dataset_id: sdsDatasetId,
      ref_p_start_date: '2017-01-01',
      ref_p_end_date: '2017-02-01',
      employment_date: '2016-06-10',
      return_by: '2017-03-01',
      ru_name: 'Apple',
      trad_as: 'Apple',
      boolean_flag: booleanFlag
    }
  }
}
