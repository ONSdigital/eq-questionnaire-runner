local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'past-usual-address-household-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'past-usual-address-household-answer',
      mandatory: false,
      options: [
        {
          label: {
            text: '{address}',
            placeholders: [
              placeholders.address,
            ],
          },
          value: '{address}',
        },
        {
          label: 'Another address in the UK',
          value: 'Another address in the UK',
        },
        {
          label: 'An address outside the UK',
          value: 'An address outside the UK',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'One year ago, on 13 October 2018, what was your usual address?';
local proxyTitle = {
  text: 'One year ago, on 13 October 2018, what was {person_name_possessive} usual address?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};


{
  type: 'Question',
  id: 'past-usual-household-address',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'another-uk-address',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'not equals',
            value: 'An address outside the UK',
          },
          rules.under16,
        ],
      },
    },
    {
      goto: {
        block: 'employment-status',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'not equals',
            value: 'An address outside the UK',
          },
          rules.over16,
        ],
      },
    },
    {
      goto: {
        block: 'employment-status',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'not equals',
            value: 'An address outside the UK',
          },
          rules.estimatedAge,
        ],
      },
    },
    {
      goto: {
        block: 'length-of-stay',
      },
    },
  ],
}
