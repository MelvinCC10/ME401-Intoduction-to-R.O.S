// Auto-generated. Do not edit!

// (in-package beginner_tutorials.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Linear = require('./Linear.js');
let Angular = require('./Angular.js');

//-----------------------------------------------------------

class Position {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.linear = null;
      this.angular = null;
    }
    else {
      if (initObj.hasOwnProperty('linear')) {
        this.linear = initObj.linear
      }
      else {
        this.linear = new Linear();
      }
      if (initObj.hasOwnProperty('angular')) {
        this.angular = initObj.angular
      }
      else {
        this.angular = new Angular();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Position
    // Serialize message field [linear]
    bufferOffset = Linear.serialize(obj.linear, buffer, bufferOffset);
    // Serialize message field [angular]
    bufferOffset = Angular.serialize(obj.angular, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Position
    let len;
    let data = new Position(null);
    // Deserialize message field [linear]
    data.linear = Linear.deserialize(buffer, bufferOffset);
    // Deserialize message field [angular]
    data.angular = Angular.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'beginner_tutorials/Position';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '3216d061298312bfbf56490a98c5cbca';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Linear linear
    Angular angular
    
    ================================================================================
    MSG: beginner_tutorials/Linear
    float32 x
    float32 y
    float32 z
    
    ================================================================================
    MSG: beginner_tutorials/Angular
    float32 roll
    float32 pitch
    float32 yaw
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Position(null);
    if (msg.linear !== undefined) {
      resolved.linear = Linear.Resolve(msg.linear)
    }
    else {
      resolved.linear = new Linear()
    }

    if (msg.angular !== undefined) {
      resolved.angular = Angular.Resolve(msg.angular)
    }
    else {
      resolved.angular = new Angular()
    }

    return resolved;
    }
};

module.exports = Position;
