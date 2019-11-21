{
  type: 'Question',
  id: 'proxy',
  question: {
    id: 'proxy-question',
    title: '<em>Interviewer Note:</em> Are they answering the questions for themselves or on someone else’s behalf?',
    type: 'General',
    answers: [
      {
        id: 'proxy-answer',
        mandatory: false,
        default: 'No, they are answering on someone else’s behalf',
        options: [
          {
            label: 'Yes, they are answering for themselves',
            value: 'Yes, they are answering for themselves',
          },
          {
            label: 'No, they are answering on someone else’s behalf',
            value: 'No, they are answering on someone else’s behalf',
          },
        ],
        type: 'Radio',
      },
    ],
  },
}
