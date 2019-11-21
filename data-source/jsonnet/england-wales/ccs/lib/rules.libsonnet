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

local estimatedAge = {
  id: 'date-of-birth-answer',
  condition: 'not set',
};

{
  isNotProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes, they are answering for themselves',
  },
  isProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No, they are answering on someone else’s behalf',
  },
  listIsEmpty: listIsEmpty,
  listIsNotEmpty: listIsNotEmpty,
  estimatedAge: estimatedAge,
} + common_rules
