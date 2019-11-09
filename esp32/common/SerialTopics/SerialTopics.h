#ifndef __SERIALTOPICS_H__
#define __SERIALTOPICS_H__

#include <Arduino.h>
#include "SerialTalks.h"

#define SERIALTOPICS_DEFAULT_TIMING 100 //ms

#define SERIALTOPICS_MAX_OPCODE 5

#define START_SUBSCRIPTION_OPCODE 0X07
#define STOP_SUBSCRIPTION_OPCODE 0X08
#define GET_SUBSCRIPTION_STATE_OPCODE 0X09

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

    static void START_SUBSCRIPTION(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void STOP_SUBSCRIPTION(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void GET_SUBSCRIPTION_STATE(SerialTalks &talks, Deserializer &input, Serializer &output);

    static void DEFAULT_HANDLER(Serializer &output);
};

extern SerialTopics topics;

#endif // __SERIALTOPICS_H__