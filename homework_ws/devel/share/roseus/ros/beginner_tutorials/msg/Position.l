;; Auto-generated. Do not edit!


(when (boundp 'beginner_tutorials::Position)
  (if (not (find-package "BEGINNER_TUTORIALS"))
    (make-package "BEGINNER_TUTORIALS"))
  (shadow 'Position (find-package "BEGINNER_TUTORIALS")))
(unless (find-package "BEGINNER_TUTORIALS::POSITION")
  (make-package "BEGINNER_TUTORIALS::POSITION"))

(in-package "ROS")
;;//! \htmlinclude Position.msg.html


(defclass beginner_tutorials::Position
  :super ros::object
  :slots (_linear _angular ))

(defmethod beginner_tutorials::Position
  (:init
   (&key
    ((:linear __linear) (instance beginner_tutorials::Linear :init))
    ((:angular __angular) (instance beginner_tutorials::Angular :init))
    )
   (send-super :init)
   (setq _linear __linear)
   (setq _angular __angular)
   self)
  (:linear
   (&rest __linear)
   (if (keywordp (car __linear))
       (send* _linear __linear)
     (progn
       (if __linear (setq _linear (car __linear)))
       _linear)))
  (:angular
   (&rest __angular)
   (if (keywordp (car __angular))
       (send* _angular __angular)
     (progn
       (if __angular (setq _angular (car __angular)))
       _angular)))
  (:serialization-length
   ()
   (+
    ;; beginner_tutorials/Linear _linear
    (send _linear :serialization-length)
    ;; beginner_tutorials/Angular _angular
    (send _angular :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; beginner_tutorials/Linear _linear
       (send _linear :serialize s)
     ;; beginner_tutorials/Angular _angular
       (send _angular :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; beginner_tutorials/Linear _linear
     (send _linear :deserialize buf ptr-) (incf ptr- (send _linear :serialization-length))
   ;; beginner_tutorials/Angular _angular
     (send _angular :deserialize buf ptr-) (incf ptr- (send _angular :serialization-length))
   ;;
   self)
  )

(setf (get beginner_tutorials::Position :md5sum-) "3216d061298312bfbf56490a98c5cbca")
(setf (get beginner_tutorials::Position :datatype-) "beginner_tutorials/Position")
(setf (get beginner_tutorials::Position :definition-)
      "Linear linear
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

")



(provide :beginner_tutorials/Position "3216d061298312bfbf56490a98c5cbca")


