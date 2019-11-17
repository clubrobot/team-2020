#include "SerialTopics.h"
#include "Clock.h"

// Global instance

SerialTopics topics;

void SerialTopics::MANAGE(SerialTalks &talks, Deserializer &input, Serializer &output)
{
    byte command = input.read<byte>();
    byte opcode = input.read<byte>();
    switch (command)
    {
    case SUBSCRIBE:
    {
        long timestep = input.read<long>();
        if (opcode < SERIALTOPICS_MAX_OPCODE)
        {
            topics.getSubscriptions()[opcode].timestep = timestep;
            topics.getSubscriptions()[opcode].lasttime = 0;
            topics.getSubscriptions()[opcode].enable = true;
            output.write<bool>(true);
        }
        else
        {
            output.write<bool>(false);
        }
        break;
    }
    case UNSUBSCRIBE:
    {
        if (opcode < SERIALTOPICS_MAX_OPCODE)
        {
            topics.getSubscriptions()[opcode].enable = false;
            output.write<bool>(true);
        }
        else
        {
            output.write<bool>(false);
        }
        break;
    }
    default:
    {
        output.write<bool>(false);
        break;
    }
    }
}

void SerialTopics::DEFAULT_HANDLER(Serializer &output)
{
}

void SerialTopics::begin(SerialTalks &talks)
{
    _talks = &talks;

    _talks->bind(MANAGE_OPCODE, MANAGE);

    for (int i = 0; i < SERIALTOPICS_MAX_OPCODE; i++)
    {
        _subscriptions[i].timestep = SERIALTOPICS_DEFAULT_TIMING;
        _subscriptions[i].lasttime = 0;
        _subscriptions[i].enable = false;
        _subscriptions[i].func = DEFAULT_HANDLER;
    }
}

void SerialTopics::bind(byte opcode, Subscription subscription)
{
    if (opcode < SERIALTOPICS_MAX_OPCODE)
        _subscriptions[opcode].func = subscription;
}

bool SerialTopics::execute()
{
    long currentTime = millis();
    for (int i = 0; i < SERIALTOPICS_MAX_OPCODE; i++)
    {
        if (_subscriptions[i].enable && currentTime - _subscriptions[i].lasttime > _subscriptions[i].timestep)
        {
            Serializer ser = _talks->getSerializer();
            _subscriptions[i].func(ser);
            _talks->send(i, ser);
            _subscriptions[i].lasttime = currentTime;
        }
    }
    return true;
}