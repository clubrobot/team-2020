#ifndef __SERIALTOPICS_H__
#define __SERIALTOPICS_H__

#include <Arduino.h>
#include "SerialTalks.h"

#define SERIALTOPICS_DEFAULT_TIMING 100 //ms

#define SERIALTOPICS_MAX_OPCODE 5

#define SUBSCRIBE_OPCODE (SERIALTALKS_RESEVED_OPCODE_7)
#define UNSUBSCRIBE_OPCODE (SERIALTALKS_RESEVED_OPCODE_8)
#define GET_CONTEXT_OPCODE (SERIALTALKS_RESEVED_OPCODE_9)

class SerialTopics
{
public:
    typedef void (*Subscription)(Serializer &output);

    typedef struct
    {
        /* data */
        Subscription func;
        long timestep;
        long lasttime;
        bool enable;
    } subscription_t;

    void begin(SerialTalks &talks);
    void bind(byte opcode, Subscription subscription);
    bool execute();

    subscription_t *getSubscriptions() { return _subscriptions; }

private:
    SerialTalks *_talks;

    subscription_t _subscriptions[SERIALTOPICS_MAX_OPCODE]; /*!< Listes des souscriptions enregistrées avec un OPCode associé.*/

    static void SUBSCRIBE(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void UNSUBSCRIBE(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void GET_CONTEXT(SerialTalks &talks, Deserializer &input, Serializer &output);

    static void DEFAULT_HANDLER(Serializer &output);
};

extern SerialTopics topics;

#endif // __SERIALTOPICS_H__