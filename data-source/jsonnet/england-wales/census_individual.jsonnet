// personal details
local accommodation_type = import '../common/blocks/individual/personal-details/accommodation_type.jsonnet';
local confirm_dob = import '../common/blocks/individual/personal-details/confirm_dob.jsonnet';
local date_of_birth = import '../common/blocks/individual/personal-details/date_of_birth.jsonnet';
local establishment_position = import '../common/blocks/individual/personal-details/establishment_position.jsonnet';
local in_education = import '../common/blocks/individual/personal-details/in_education.jsonnet';
local name = import '../common/blocks/individual/personal-details/name.jsonnet';
local proxy = import '../common/blocks/individual/personal-details/proxy.jsonnet';
local address_type = import 'blocks/individual/personal-details/address_type.jsonnet';
local another_address = import 'blocks/individual/personal-details/another_address.jsonnet';
local current_marriage_status = import 'blocks/individual/personal-details/current_marriage_status.jsonnet';
local current_partnership_status = import 'blocks/individual/personal-details/current_partnership_status.jsonnet';
local marriage_type = import 'blocks/individual/personal-details/marriage_type.jsonnet';
local other_uk_address = import 'blocks/individual/personal-details/other_uk_address.jsonnet';
local previous_marriage_status = import 'blocks/individual/personal-details/previous_marriage_status.jsonnet';
local previous_partnership_status = import 'blocks/individual/personal-details/previous_partnership_status.jsonnet';
local sex = import 'blocks/individual/personal-details/sex.jsonnet';
local term_time_address_country = import 'blocks/individual/personal-details/term_time_address_country.jsonnet';
local term_time_address_details = import 'blocks/individual/personal-details/term_time_address_details.jsonnet';
local term_time_location = import 'blocks/individual/personal-details/term_time_location.jsonnet';

// identity and health
local health = import '../common/blocks/individual/identity-and-health/health.jsonnet';
local last_year_address = import '../common/blocks/individual/identity-and-health/last_year_address.jsonnet';
local passports = import '../common/blocks/individual/identity-and-health/passports.jsonnet';
local speak_english = import '../common/blocks/individual/identity-and-health/speak_english.jsonnet';
local arrive_in_country = import 'blocks/individual/identity-and-health/arrive_in_country.jsonnet';
local birth_gender = import 'blocks/individual/identity-and-health/birth_gender.jsonnet';
local carer = import 'blocks/individual/identity-and-health/carer.jsonnet';
local country_of_birth = import 'blocks/individual/identity-and-health/country_of_birth.jsonnet';
local disability = import 'blocks/individual/identity-and-health/disability.jsonnet';
local disability_limitation = import 'blocks/individual/identity-and-health/disability_limitation.jsonnet';
local ethnic_group = import 'blocks/individual/identity-and-health/ethnic_group.jsonnet';
local ethnic_group_asian = import 'blocks/individual/identity-and-health/ethnic_group_asian.jsonnet';
local ethnic_group_black = import 'blocks/individual/identity-and-health/ethnic_group_black.jsonnet';
local ethnic_group_mixed = import 'blocks/individual/identity-and-health/ethnic_group_mixed.jsonnet';
local ethnic_group_other = import 'blocks/individual/identity-and-health/ethnic_group_other.jsonnet';
local ethnic_group_white = import 'blocks/individual/identity-and-health/ethnic_group_white.jsonnet';
local language = import 'blocks/individual/identity-and-health/language.jsonnet';
local length_of_stay = import 'blocks/individual/identity-and-health/length_of_stay.jsonnet';
local national_identity = import 'blocks/individual/identity-and-health/national_identity.jsonnet';
local past_usual_household_address = import 'blocks/individual/identity-and-health/past_usual_household_address.jsonnet';
local religion = import 'blocks/individual/identity-and-health/religion.jsonnet';
local sexual_identity = import 'blocks/individual/identity-and-health/sexual_identity.jsonnet';
local understand_welsh = import 'blocks/individual/identity-and-health/understand_welsh.jsonnet';
local when_arrive_in_uk = import 'blocks/individual/identity-and-health/when_arrive_in_uk.jsonnet';

// qualifications
local a_level = import 'blocks/individual/qualifications/a_level.jsonnet';
local apprenticeship = import 'blocks/individual/qualifications/apprenticeship.jsonnet';
local degree = import 'blocks/individual/qualifications/degree.jsonnet';
local gcse = import 'blocks/individual/qualifications/gcse.jsonnet';
local nvq_level = import 'blocks/individual/qualifications/nvq_level.jsonnet';
local other_qualifications = import 'blocks/individual/qualifications/other_qualifications.jsonnet';
local qualifications = import 'blocks/individual/qualifications/qualifications.jsonnet';

// employment
local business_name = import '../common/blocks/individual/employment/business_name.jsonnet';
local employer_address_depot = import '../common/blocks/individual/employment/employer_address_depot.jsonnet';
local employer_address_workplace = import '../common/blocks/individual/employment/employer_address_workplace.jsonnet';
local employment_status = import '../common/blocks/individual/employment/employment_status.jsonnet';
local employment_type = import '../common/blocks/individual/employment/employment_type.jsonnet';
local hours_worked = import '../common/blocks/individual/employment/hours_worked.jsonnet';
local job_availability = import '../common/blocks/individual/employment/job_availability.jsonnet';
local job_description = import '../common/blocks/individual/employment/job_description.jsonnet';
local job_pending = import '../common/blocks/individual/employment/job_pending.jsonnet';
local job_title = import '../common/blocks/individual/employment/job_title.jsonnet';
local jobseeker = import '../common/blocks/individual/employment/jobseeker.jsonnet';
local main_employment_block = import '../common/blocks/individual/employment/main_employment_block.jsonnet';
local main_job_type = import '../common/blocks/individual/employment/main_job_type.jsonnet';
local supervise = import '../common/blocks/individual/employment/supervise.jsonnet';
local work_travel = import '../common/blocks/individual/employment/work_travel.jsonnet';
local armed_forces = import 'blocks/individual/employment/armed_forces.jsonnet';
local employer_type_of_address = import 'blocks/individual/employment/employer_type_of_address.jsonnet';
local employers_business = import 'blocks/individual/employment/employers_business.jsonnet';
local ever_worked = import 'blocks/individual/employment/ever_worked.jsonnet';

local comments = import '../common/blocks/comments.json';

local understandWelshBlock(region_code) = if region_code == 'GB-WLS' then [understand_welsh] else [];

function(region_code, census_date) {
  mime_type: 'application/json/ons/eq',
  schema_version: '0.0.1',
  data_version: '0.0.3',
  survey_id: 'census',
  title: '2019 Census Test',
  description: 'Census England Individual Schema',
  theme: 'census',
  legal_basis: 'Voluntary',
  navigation: {
    visible: false,
  },
  metadata: [
    {
      name: 'user_id',
      type: 'string',
    },
    {
      name: 'period_id',
      type: 'string',
    },
    {
      name: 'case_type',
      type: 'string',
      optional: true,
    },
    {
      name: 'display_address',
      type: 'string',
    },

  ],
  sections: [
    {
      id: 'individual-section',
      title: 'Individual Section',
      groups: [
        {
          id: 'personal-details-group',
          title: 'Personal Details',
          blocks: [
            accommodation_type,
            proxy,
            name,
            establishment_position,
            date_of_birth(census_date),
            confirm_dob,
            sex,
            marriage_type(census_date),
            current_marriage_status,
            previous_marriage_status,
            current_partnership_status,
            previous_partnership_status,
            another_address,
            other_uk_address,
            address_type,
            in_education,
            term_time_location,
            term_time_address_country,
            term_time_address_details,
          ],
        },
        {
          id: 'identity-and-health-group',
          title: 'Identity and Health',
          blocks: [
            country_of_birth(region_code),
            arrive_in_country(region_code, census_date),
            when_arrive_in_uk(region_code, census_date),
            length_of_stay(region_code),
          ] + understandWelshBlock(region_code) + [
            language(region_code),
            speak_english,
            national_identity(region_code),
            ethnic_group(region_code),
            ethnic_group_white(region_code),
            ethnic_group_mixed,
            ethnic_group_asian,
            ethnic_group_black,
            ethnic_group_other,
            religion(region_code),
            past_usual_household_address,
            last_year_address,
            passports,
            health,
            disability,
            disability_limitation,
            carer,
            sexual_identity,
            birth_gender,
          ],
        },
        {
          id: 'qualifications-group',
          title: 'Qualifications',
          blocks: [
            qualifications(region_code),
            apprenticeship(region_code),
            degree(region_code),
            nvq_level(region_code),
            a_level(region_code),
            gcse(region_code),
            other_qualifications(region_code),
          ],
        },
        {
          id: 'employment-group',
          title: 'Employment',
          blocks: [
            armed_forces,
            employment_status,
            employment_type,
            jobseeker,
            job_availability,
            job_pending,
            ever_worked,
            main_employment_block,
            main_job_type,
            business_name,
            job_title,
            job_description,
            employers_business(region_code),
            supervise,
            hours_worked,
            work_travel,
            employer_type_of_address,
            employer_address_workplace,
            employer_address_depot,
          ],
        },
      ],
    },
    {
      id: 'comments',
      title: 'Comments',
      groups: [
        {
          blocks: [
            comments,
          ],
          id: 'comments-group',
          title: 'Comments',
        },
      ],
    },
    {
      id: 'submit-answers-section',
      title: 'Submit answers',
      groups: [
        {
          id: 'submit-group',
          title: 'Submit answers',
          blocks: [
            {
              id: 'summary',
              type: 'Summary',
            },
          ],
        },
      ],
    },
  ],
}
