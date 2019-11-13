local common_rules = import '../../lib/common_rules.libsonnet';

local listIsEmpty(listName) = {
  list: listName,
  condition: 'equals',
  value: 0,
};

local listIsNotEmpty(listName) = {
  list: listName,
  condition: 'greater than',
  value: 0,
};

{
  isNotProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes, I am',
  },
  isProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No, I am answering on their behalf',
  },
  listIsEmpty: listIsEmpty,
  listIsNotEmpty: listIsNotEmpty,
} + common_rules
