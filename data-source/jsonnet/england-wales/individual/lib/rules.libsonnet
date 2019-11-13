local common_rules = import '../../lib/common_rules.libsonnet';

{
  isNotProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No, I’m answering for myself',
  },
  isProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes',
  },
} + common_rules
